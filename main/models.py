from typing import Union, Dict, Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from multiselectfield import MultiSelectField
from . import field_choices as choices
from .translations import ORDER_STATUS

class ProductPhoto(models.Model):
    url = models.URLField('URL')

    def __str__(self):
        return self.url

class Product(models.Model):
    name = models.CharField('Name', max_length=100, unique=True)
    main_photo = models.OneToOneField(ProductPhoto, on_delete=models.PROTECT, verbose_name='Main photo', related_name='product2')
    photos = models.ManyToManyField(ProductPhoto, blank=True, verbose_name='Photos', related_name='product')
    price = models.FloatField('Price')
    discount = models.FloatField('Discount', blank=True, default=0)
    avr_rating = models.FloatField('Avarange rating', blank=True, default=0)
    date_of_issue = models.DateField('Date of issue')
    quantity = models.IntegerField('Quantity')

    def get_price(self):
        return f'{self.price:.2f}'.replace(',', '.')
    
    def get_rating(self):
        return f'{self.avr_rating:.1f}'.replace(',', '.')
    
    def get_discount(self):
        return f'-{int(self.discount * 100)}%'
    
    def get_discount_price(self):
        dicount_price = self.price - self.price * self.discount
        return f'{dicount_price:.2f}'.replace(',', '.')
    
    def get_date_of_issue(self):
        return self.date_of_issue.strftime('%d.%m.%Y')

    @staticmethod
    def __set_attr(attr:str, ids:Iterable[int], colections:Union[Iterable, Dict[str, Union[str,Iterable]]]):
        '''
        Sets a boolean value for the `field` attribute for products from `collections`,
        indicating whether the product's identifier belongs to the `ids` list.

        product.`field` = product.id in `ids`
        '''
        
        for colection in colections:
            if isinstance(colection, dict):
                for item in colection['queryset']:
                    product = getattr(item, colection['field'])
                    setattr(product, attr, product.id in ids)
            else:
                for product in colection:
                    setattr(product, attr, product.id in ids)

    @staticmethod
    def set_is_favorite_attr(user, *colections:Union[Iterable,Dict[str, Union[str,Iterable]]]):
        '''
        Set the `is_favorite` attribute for products from `collections`,
        indicating whether the product is in the favorites of the `user`.
        '''

        if isinstance(user, User):
            ids = user.favorites.values_list('id', flat=True)
        else:
            ids = tuple()
        
        Product.__set_attr('is_favorite', ids, colections)
    
    @staticmethod
    def set_is_in_cart_attr(user, *colections:Union[Iterable,Dict[str, Union[str,Iterable]]]):
        '''
        Set the `is_in_cart` attribute for products from `collections`,
        indicating whether the product is in the cart of the `user`.
        '''

        if isinstance(user, User):
            ids = CartProduct.objects.filter(user__id=user.id).values_list('product__id', flat=True)
        else:
            ids = tuple()
        
        Product.__set_attr('is_in_cart', ids, colections)

    def __str__(self):
        return self.name

class Characteristic(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='characteristic')
    colors  = models.CharField('Colors', max_length=70)

    # Main
    manufacturer = models.CharField('Manufacturer', max_length=10, choices=choices.MANUFACTURERS)
    os           = models.CharField('OS', max_length=10, choices=choices.OPERATING_SYSTEMS)

    # Display
    diagonal              = models.FloatField('Diagonal (")')
    horizontal_resolution = models.IntegerField('Horizontal resolution (px)')
    vertical_resolution   = models.IntegerField('Vertical resolution (px)')
    matrix                = models.CharField('Matrix', max_length=10, choices=choices.MATRICES)
    screen_frequency      = models.IntegerField('Screen frequency(GHz)')
    screen_material       = models.CharField('Screen material', max_length=50)

    # Connection
    connection_types = MultiSelectField('Connection types', null=True, blank=True, choices=choices.CONNECTION_TYPES)
    sim_number       = models.IntegerField('Number of SIM', choices=choices.SIM_NUMBERS)
    sim_size         = models.CharField('SIM size', max_length=5, choices=choices.SIM_SIZES)

    # Memory
    ram = models.IntegerField('RAM (Gb)')
    rom = models.IntegerField('ROM (Gb)')
    additional_memory = models.CharField('Additional memory', max_length=20)
    max_size_additional_memory = models.IntegerField('Max size of additional memory (Gb)')

    # Main camera
    main_camera           = models.IntegerField('Main camera (Mp)')
    number_main_cameras   = models.IntegerField('Number of main cameras', choices=choices.NUMBER_OF_CAMERAS)
    main_camera_features  = MultiSelectField('Features of main camera', null=True, blank=True, choices=choices.MAIN_CAMERA_FEATURES)
    main_camera_video     = models.CharField('Main camera video', max_length=80)
    main_camera_additions_en = models.TextField('Main camera additions (en)', null=True, blank=True)
    main_camera_additions_ua = models.TextField('Main camera additions (ua)', null=True, blank=True)

    # Front camera
    front_camera       = models.IntegerField('Front camera (Mp)')
    front_camera_video = models.CharField('Front video', max_length=80)
    front_camera_additions_en = models.TextField('Front camera additions (en)', null=True, blank=True)
    front_camera_additions_ua = models.TextField('Front camera additions (ua)', null=True, blank=True)

    # Processor
    processor    = models.CharField('Processor', max_length=50)
    videocore    = models.CharField('Videocore', max_length=50)
    number_cores = models.IntegerField('Number of cores')
    processor_frequency = models.FloatField('Processor frequency (GHz)')

    # Dimensions
    weight = models.FloatField('Weight (g)')
    width  = models.FloatField('Width (mm)')
    height = models.FloatField('Height (mm)')
    depth  = models.FloatField('Depth (mm)')

    # Addition
    battery_volume = models.IntegerField('Battery volume (mAh)')
    wirelesses = MultiSelectField('Wireless',   null=True, blank=True, choices=choices.WIRELESSES)
    connectors = MultiSelectField('Connectors', null=True, blank=True, choices=choices.CONNECTORS)
    security   = MultiSelectField('Security',   null=True, blank=True, choices=choices.SECURITY)
    protection = models.CharField('Protection', max_length=20)
    sensors_en    = models.TextField('Sensors (en)')
    sensors_ua    = models.TextField('Sensors (ua)')
    
    features      = MultiSelectField('Features',   null=True, blank=True, choices=choices.FEATURES)
    additions_en  = models.TextField('Additions (en)', null=True, blank=True,)
    additions_ua  = models.TextField('Additions (ua)', null=True, blank=True,)

    def get_first_color(self):
        index = self.colors.find(';')
        if index == -1:
            return self.colors
        return self.colors[:index]
    
    def get_colors(self):
        return self.colors.split(';')
    
    def __str__(self):
        return self.product.name

class UserManager(BaseUserManager):
    def create_user(self, email:str, password:str, commit=True, **extra_fields:str):
        if not email or not password:
            raise ValueError('email and password is not be empty')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if commit:
            user.save()
        return user
    
    def create_superuser(self, email:str, password:str, **extra_fields:str):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    password = models.CharField('Password', max_length=100)
    name = models.CharField('Name', max_length=20)
    phone = models.CharField('Phone', max_length=12)
    address = models.CharField('Address', null=True, blank=True, max_length=150)
    favorites = models.ManyToManyField(Product, blank=True, verbose_name='Favorites', related_name='favorites')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class BrowsedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='browsed_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='users_browsed')
    datetime = models.DateTimeField('Date and time')

    def get_datetime(self):
        return self.datetime.strftime('%d.%m.%Y - %H:%M')

    def __str__(self):
        return f'{self.user.email} - {self.product.name}'

class Order(models.Model):
    STATUS_CHOICES = (
        ('is confirmed', 'Is confirmed'),
        ('on the way',   'On the way'),
        ('arrived',      'Arrived'),
        ('canceled',     'Canceled'),
    )

    STATUS_COLORS = {
        'is confirmed': '80 60 95',
        'on the way':   '195 170 0',
        'arrived':      '70 180 0',
        'canceled':     '180 20 0',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='orders')
    product_price = models.FloatField('Product price')
    color = models.CharField('Color', max_length=6)
    quantity = models.IntegerField('Quantity')
    datetime = models.DateTimeField('Date and time')
    status = models.CharField('Status', max_length=12, choices=STATUS_CHOICES)

    def is_can_cancel(self):
        return self.status == 'is confirmed'
    
    def is_can_delete(self):
        return self.status == 'canceled' or self.status == 'arrived'

    def get_total_price(self):
        return f'{(self.product_price * self.quantity):.2f}'.replace(',', '.')

    @staticmethod
    def set_attrs_for_view(orders:Iterable, lang:str):
        for order in orders:
            order.status_title = ORDER_STATUS[order.status][lang]
            order.status_color = Order.STATUS_COLORS[order.status]
            if hasattr(order, 'product_price'):
                order.price_title = str(order.product_price).replace(',', '.')

    def __str__(self):
        return f'{self.user.email} - {self.product.name}'

class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='cart_products')
    color = models.CharField('Color', max_length=6)
    quantity = models.IntegerField('Quantity')
    datetime = models.DateTimeField('Date and time')

    def get_total_price(self):
        price = self.product.price * self.quantity

        if self.product.discount:
            price -= price * self.product.discount

        return f'{price:.2f}'.replace(',', '.')
    
    def __str__(self):
        return f'{self.user.email} - {self.product.name}'

class Feedback(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, verbose_name='User', related_name='feedback')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='feedbacks')
    rating = models.IntegerField('Rating')
    description = models.TextField('Description', null=True, blank=True)
    datetime = models.DateTimeField('Date and time')

    def __str__(self):
        return f'{self.user.email if self.user else "(Deleted)"} - {self.product.name}'

class Question(models.Model):
    CATEGORY_CHOICES = (
        ('shop',    'Shop'),
        ('deliver', 'Deliver'),
        ('other',   'Other')
    )
    category = models.CharField('Category', max_length=10, choices=CATEGORY_CHOICES)
    question_en = models.CharField('Question (en)', max_length=100)
    question_ua = models.CharField('Question (ua)', max_length=100)
    responce_en = models.CharField('Responce (en)', max_length=500)
    responce_ua = models.CharField('Responce (ua)', max_length=500)

    @staticmethod
    def set_question_and_responce_attr(lang:str, *colections:Iterable):
        for colection in colections:
            for model in colection:
                model.question = getattr(model, f'question_{lang}')
                model.responce = getattr(model, f'responce_{lang}')

    def __str__(self):
        return self.question_en