from typing import Union, Dict, Any, Type, Optional
from abc import ABC
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
import json
from datetime import datetime
from .tools import get
from .services import APIAuthActions, APIProductActions, APIUserDataActions
from . import models
from . import products_componer
from . import translations as trsl

class MenuItems(ABC):
    HOME     = 'Home'
    PRODUCTS = 'Products'
    FAQ      = 'FAQ'
    ACCOUNT  = 'Account'
    CART     = 'Cart'

    @staticmethod
    def get_products_in_cart_count(user:models.User) -> Optional[int]:
        return user.cart_products.count() if user.is_authenticated else None
    
class SidemenuItems(ABC):
    INFO      = 'Info'
    CART      = 'Cart'
    ORDERS    = 'Orders'
    FAVORITES = 'Favorites'
    HISTORY   = 'History'

class MsgColors(ABC):
    INFO    = '0, 95, 165'
    ERROR   = '255, 0, 65'
    SUCCESS = '0, 135, 50'
    WARNING = '210, 180, 55'

def __get_lang_and_layout_labels(request:HttpRequest):
    '''
    Returns the user's selected language (`str`) and labels for layout.html in that language (`Dict[str,str]`).
    '''

    lang = get(request.COOKIES, key='lang', default='en')
    
    if not lang in ('en', 'ua'):
        lang = 'en'

    layout_labels = trsl.select_labels_by_lang(trsl.LAYOUT_LABELS, lang)
    layout_labels['lang'] = lang
    return lang, layout_labels

def index(request:HttpRequest):
    new_products = models.Product.objects.order_by('-date_of_issue')[:10].only(
        'name', 'main_photo', 'price', 'discount', 'avr_rating'
    )
    discount_products = models.Product.objects.filter(discount__gt=0).order_by('-discount')[:10].only(
        'name', 'main_photo', 'price', 'discount', 'avr_rating'
    )

    models.Product.set_is_favorite_attr(request.user, new_products, discount_products)
    models.Product.set_is_in_cart_attr(request.user, new_products, discount_products)
    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'active_menu_item':  MenuItems.HOME,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(request.user),
        'new_products':      new_products,
        'discount_products': discount_products,
        'layout_labels':     layout_labels,
        'labels':            trsl.select_labels_by_lang(trsl.HOME_LABELS, lang),
    }

    return render(request, 'main/index.html', context)

def products(request:HttpRequest):
    # Get products and pages data
    products = products_componer.get_filtered_and_sort_products(request.GET)
    page, all_pages, products = products_componer.get_activePage_allPages_productsFromPage(products, request.GET)

    products = products.select_related('main_photo').only(
        'name', 'main_photo', 'price', 'discount', 'avr_rating'
    )

    # Browsing products
    user = request.user

    if user.is_authenticated:
        browsed_products = user.browsed_products.order_by('-datetime')[:10]
        browsed_products.select_related('product').only(
            'product__name', 'product__main_photo', 'product__price', 'product__discount', 'product__avr_rating'
        )
        browsed_products = tuple(bp.product for bp in browsed_products)
    else:
        browsed_products = tuple()

    models.Product.set_is_favorite_attr(user, products, browsed_products)
    models.Product.set_is_in_cart_attr(user, products, browsed_products)

    # render view
    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'active_menu_item': MenuItems.PRODUCTS,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'filters_data':     products_componer.get_filters_for_view(lang),
        'params':           json.dumps(request.GET),
        'products':         products,
        'browsed_products': browsed_products,
        'active_page':      page,
        'all_pages':        all_pages,
        'layout_labels':    layout_labels,
        'labels':           trsl.select_labels_by_lang(trsl.PRODUCTS_LABELS, lang),
    }

    return render(request, 'main/products.html', context)

def faq(request:HttpRequest):
    lang, layout_labels = __get_lang_and_layout_labels(request)

    shop_questions    = models.Question.objects.filter(category='shop').only(f'question_{lang}', f'responce_{lang}')
    deliver_questions = models.Question.objects.filter(category='deliver').only(f'question_{lang}', f'responce_{lang}')
    other_questions   = models.Question.objects.filter(category='other').only(f'question_{lang}', f'responce_{lang}')

    models.Question.set_question_and_responce_attr(lang, shop_questions, deliver_questions, other_questions)

    context = {
        'active_menu_item':  MenuItems.FAQ,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(request.user),
        'shop_questions':    shop_questions,
        'deliver_questions': deliver_questions,
        'other_questions':   other_questions,
        'layout_labels':     layout_labels,
        'labels':            trsl.select_labels_by_lang(trsl.FAQ_LABELS, lang),
    }

    return render(request, 'main/faq.html', context)

def product(request:HttpRequest):
    # check and get product
    if (not 'id' in request.GET) or (not request.GET['id'].isdigit()):
        return redirect('home')
    
    product_id = int(request.GET['id'])
    try:
        product = models.Product.objects.get(id=product_id)
        characteristic = models.Characteristic.objects.get(id=product.characteristic.id)
    except ObjectDoesNotExist:
        return redirect('home')
    
    # get feedbacks and check favorite
    feedbacks = models.Feedback.objects.filter(product__id=product_id).order_by('-datetime')
    feedbacks_count = feedbacks.count()
    user = request.user
    user_feedback = None

    if user.is_authenticated:
        product.is_favorite = user.favorites.filter(id=product_id).exists()

        try:
            user_feedback = models.Feedback.objects.get(id=user.feedback.id)
            feedbacks = feedbacks.exclude(user__id=user.id)
        except ObjectDoesNotExist:
            pass

        # add to browsing products
        user_browsed_products = user.browsed_products.all()
        try:
            browsed_product = user_browsed_products.get(product__id=product_id)
            browsed_product.datetime = datetime.now()
            browsed_product.save(update_fields=('datetime',))
        except ObjectDoesNotExist:
            if user_browsed_products.count() == 30:
                user_browsed_products.order_by('datetime').first().delete()
            models.BrowsedProduct.objects.create(
                user=user,
                product=product,
                datetime=datetime.now()
            )

    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'product':        product,
        'colors':         characteristic.get_colors(),
        'characteristic': products_componer.get_characteristic_for_view(characteristic, lang),
        'photos':         product.photos.values_list('url', flat=True),
        'feedbacks':      feedbacks.values('user__name', 'rating', 'description'),
        'feedbacks_count': feedbacks_count,
        'user_feedback':  user_feedback,
        'layout_labels':  layout_labels,
        'labels':         trsl.select_labels_by_lang(trsl.PRODUCT_LABELS, lang),
    }

    return render(request, 'main/product.html', context)

def user_info(request:HttpRequest):
    if not request.user.is_authenticated:
        return redirect('auth')
    
    user = request.user
    address_parts = user.address.split(';;') if user.address else ('', '', '')
    city, street, index = address_parts

    fields_data = {
        'name': user.name,
        'phone': user.phone,
        'email': user.email,
        'city': city,
        'street': street,
        'index': index,
    }

    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'active_menu_item':       MenuItems.ACCOUNT,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'active_sidemenu_item':   SidemenuItems.INFO,
        'fields_data':            fields_data,
        'layout_labels':          layout_labels,
        'labels':                 trsl.select_labels_by_lang(trsl.USER_INFO_LABELS, lang),
        'sidemenu_labels':        trsl.select_labels_by_lang(trsl.SIDEMENU_LABELS, lang),
    }

    return render(request, 'main/user_info.html', context)

def cart(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect('auth')

    cart_products = user.cart_products.order_by('-datetime').select_related('product').only(
        'color', 'quantity',
        'product__name', 'product__main_photo', 'product__price', 'product__discount'
    )
    models.Product.set_is_favorite_attr(user, {'queryset': cart_products, 'field': 'product'})

    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'active_menu_item':       MenuItems.CART,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'active_sidemenu_item':   SidemenuItems.CART,
        'cart_products':          cart_products,
        'layout_labels':          layout_labels,
        'labels':                 trsl.select_labels_by_lang(trsl.ITEMS_LABELS, lang),
        'sidemenu_labels':        trsl.select_labels_by_lang(trsl.SIDEMENU_LABELS, lang),
    }

    return render(request, 'main/cart.html', context)

def orders(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect('auth')
    
    orders = user.orders.order_by('-datetime').select_related('product').only(
        'product_price', 'color', 'quantity', 'status',
        'product__name', 'product__main_photo', 'product__discount'
    )

    lang, layout_labels = __get_lang_and_layout_labels(request)
    models.Order.set_attrs_for_view(orders, lang)

    context = {
        'active_menu_item': MenuItems.ACCOUNT,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'active_sidemenu_item':   SidemenuItems.ORDERS,
        'orders':           orders,
        'layout_labels':    layout_labels,
        'labels':           trsl.select_labels_by_lang(trsl.ITEMS_LABELS, lang),
        'sidemenu_labels':  trsl.select_labels_by_lang(trsl.SIDEMENU_LABELS, lang),
    }

    return render(request, 'main/orders.html', context)

def favorites(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect('auth')
    
    products = user.favorites.select_related('main_photo').only(
        'name', 'main_photo', 'price', 'discount'
    )
    models.Product.set_is_in_cart_attr(user, products)

    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'active_menu_item': MenuItems.ACCOUNT,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'active_sidemenu_item':   SidemenuItems.FAVORITES,
        'products':         products,
        'layout_labels':    layout_labels,
        'labels':           trsl.select_labels_by_lang(trsl.ITEMS_LABELS, lang),
        'sidemenu_labels':  trsl.select_labels_by_lang(trsl.SIDEMENU_LABELS, lang),
    }

    return render(request, 'main/favorites.html', context)

def browsed_products(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect('auth')
    
    browsed_products = user.browsed_products.order_by('-datetime').select_related('product').only(
        'datetime', 'product__name', 'product__main_photo', 'product__price', 'product__discount'
    )
    
    models.Product.set_is_favorite_attr(user, {'queryset': browsed_products, 'field': 'product'})
    models.Product.set_is_in_cart_attr(user, {'queryset': browsed_products, 'field': 'product'})

    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'active_menu_item': MenuItems.ACCOUNT,
        'products_in_cart_count': MenuItems.get_products_in_cart_count(user),
        'active_sidemenu_item':   SidemenuItems.HISTORY,
        'browsed_products': browsed_products,
        'layout_labels':    layout_labels,
        'labels':           trsl.select_labels_by_lang(trsl.ITEMS_LABELS, lang),
        'sidemenu_labels':  trsl.select_labels_by_lang(trsl.SIDEMENU_LABELS, lang),
    }

    return render(request, 'main/browsed_products.html', context)

def auth(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    
    lang, layout_labels = __get_lang_and_layout_labels(request)

    context = {
        'layout_labels': layout_labels,
        'labels':        trsl.select_labels_by_lang(trsl.AUTH_LABELS, lang),
    }

    return render(request, 'main/auth.html', context)

def auth_logout(request:HttpRequest):
    logout(request)
    return redirect('home')


def __clean_api_request(request:HttpRequest, method:str, **params:Type[Union[str,int,float,None]]) -> Union[Dict[str, Any], JsonResponse]:
    '''
    Check request `method`, `parameters` and that types, in `request` url (GET) or body (other method)
    then returns dictionary with that `parameters`. If cheking is wrong than return json responce.
    '''

    if request.method != method:
        return JsonResponse({'error': 'Method do not support'}, status=405)

    if method == 'GET':
        data = dict(request.GET)
    else:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Json do not reading'}, status=400)
    
    for param in params:
        if not param in data:
            return JsonResponse({'error': f'Parameter "{param}" is not found'}, status=400)

        if params[param] != None:
            if method == 'GET':
                try:
                    data[param] = params[param](data[param])
                except ValueError:
                    return JsonResponse({'error': f'Incorret type of parameter "{param}"'}, status=400)
            else:
                if not isinstance(data[param], params[param]):
                    return JsonResponse({'error': f'Incorret type of parameter "{param}"'}, status=400)
    
    return data

def api_auth(request:HttpRequest):
    if request.user.is_authenticated:
        return JsonResponse({'error': 'User is already authenticated'}, status=401)

    # clean request and get product
    data = __clean_api_request(request, 'POST', action=str)
    if isinstance(data, JsonResponse):
        return data
    
    # action processing
    if data['action'] == 'login':
        return APIAuthActions.login(request, data)
    
    elif data['action'] == 'register':
        return APIAuthActions.register(request, data)

    return JsonResponse({'error': 'Incorrect parameter "action"'}, status=400)

def api_user_data(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

    # clean request and get product
    data = __clean_api_request(request, 'POST', action=str)
    if isinstance(data, JsonResponse):
        return data
    
    lang = get(request.COOKIES, key='lang', default='en')
    
    # action processing
    if data['action'] == 'change_info':
        return APIUserDataActions.change_info(user, data, lang)
    
    elif data['action'] == 'change_password':
        return APIUserDataActions.change_password(request, user, data, lang)
    
    elif data['action'] == 'change_address':
        return APIUserDataActions.change_address(user, data, lang)

    return JsonResponse({'error': 'Incorrect parameter "action"'}, status=400)

def api_product(request:HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

    # clean request and get product
    data = __clean_api_request(request, 'POST', action=str)
    if isinstance(data, JsonResponse):
        return data
    
    lang = get(request.COOKIES, key='lang', default='en')

    # action processing
    if data['action'] == 'favorite_add':
        return APIProductActions.favorite_add(user, data, lang)
    
    elif data['action'] == 'favorite_remove':
        return APIProductActions.favorite_remove(user, data, lang)

    elif data['action'] == 'cart_add':
        return APIProductActions.cart_add(user, data, lang)
    
    elif data['action'] == 'cart_remove':
        return APIProductActions.cart_remove(user, data, lang)

    elif data['action'] == 'cart_quantity':
        return APIProductActions.cart_quantity(user, data)

    elif data['action'] == 'order_add':
        return APIProductActions.order_add(user, data, lang)
    
    elif data['action'] == 'order_cancel':
        return APIProductActions.order_cancel(user, data, lang)

    elif data['action'] == 'order_remove':
        return APIProductActions.order_remove(user, data, lang)
    
    elif data['action'] == 'browsed_remove':
        return APIProductActions.browsed_remove(user, data, lang)
        
    return JsonResponse({'error': 'Incorrect parameter "action"'}, status=400)

def api_products(request:HttpRequest):
    # get products and pages data
    products = products_componer.get_filtered_and_sort_products(request.GET)
    page, all_pages, products = products_componer.get_activePage_allPages_productsFromPage(products, request.GET)

    products = products.only('name', 'main_photo', 'price', 'discount', 'avr_rating')

    models.Product.set_is_favorite_attr(request.user, products)
    models.Product.set_is_in_cart_attr(request.user, products)

    # create response
    response = {
        'pages': { 'active_page': page, 'all_pages': all_pages },
        'products': {},
    }

    for i in range(len(products)):
        response['products'][i] = {
            'id':            products[i].id,
            'name':          products[i].name,
            'photoURL':      products[i].main_photo.url,
            'price':         products[i].get_price(),
            'rating':        products[i].get_rating(),
            'discount':      products[i].get_discount() if products[i].discount > 0 else None,
            'discountPrice': products[i].get_discount_price() if products[i].discount > 0 else None,
            'is_favorite':   products[i].is_favorite,
            'is_in_cart':    products[i].is_in_cart,
        }

    return JsonResponse(response)

def api_feedback(request:HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

    # clean request and get product
    data = __clean_api_request(request, 'POST', product_id=int, rating=int, desc=str)
    if isinstance(data, JsonResponse):
        return data

    if data['rating'] < 1 or data['rating'] > 5:
        return JsonResponse({'error': 'Parameter "rating" out of range'}, status=400)
    
    try:
        product = models.Product.objects.defer().get(id=data['product_id'])
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # save feedback
    try:
        feedback = models.Feedback.objects.defer().get(user=request.user)
    except ObjectDoesNotExist:
        feedback = models.Feedback(user=request.user, product=product)

    feedback.rating = data['rating']
    feedback.description = data['desc']
    feedback.datetime = datetime.now()
    feedback.save()
    
    # update product rating
    avg = models.Feedback.objects.aggregate(rating=Avg('rating'))
    product.avr_rating = avg['rating']
    product.save(update_fields=('avr_rating',))

    # return response
    lang = get(request.COOKIES, key='lang', default='en')

    if not lang in ('en', 'ua'):
        lang = 'en'

    return JsonResponse({'message': trsl.PRODUCTS_MSG['feedback_saved'][lang]})

def api_lang(request:HttpRequest):
    data = __clean_api_request(request, 'POST', lang=str)

    if isinstance(data, JsonResponse):
        return data
    
    if not data['lang'] in ('en', 'ua'):
        return JsonResponse({'error': 'Incorret parameter "lang"'}, status=400)

    response = JsonResponse({'message': f'Language is {data["lang"]}'})
    response.set_cookie('lang', data['lang'])
    return response