from typing import Dict, Any
from abc import ABC
from random import randint
from django.contrib.auth import login
from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from django.core.cache import cache
from django.core.mail import send_mail
from datetime import datetime
from .tools import get
from . import models
from . import translations as trsl

def _check_params(data:Dict[str,Any], **params:type):
    '''
    If all parameters in `params` are found in the `data`
    and all parameter types match, then return `None`. Otherwise, return a JSON response.
    '''

    for param in params:
        if not param in data:
            return JsonResponse({'error': f'Parameter "{param}" is not found'}, status=400)
            
        if not isinstance(data[param], params[param]):
            return JsonResponse({'error': f'Incorret type of parameter "{param}"'}, status=400)

    return None

def _is_xss(text:str) -> bool:
    'Return `True` if the `text` contains script or style tags. Otherwise return `False`.'

    text = text.lower()
    return text.find('<script') != -1 or text.find('<style') != -1

class APIAuthActions(ABC):
    @staticmethod
    def __is_valid_email(email:str) -> bool:
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def login(request:HttpRequest, data:Dict[str,Any]):
        error = _check_params(data, email=str, password=str)
        if error: return error

        lang = get(request.COOKIES, key='lang', default='en')
        try:
            user = models.User.objects.defer().get(email=data['email'].lower())
        except ObjectDoesNotExist:
            return JsonResponse({'error': trsl.AUTH_MSG['email_not_found'][lang]}, status=404)

        if not user.check_password(data['password']):
            return JsonResponse({'error': trsl.AUTH_MSG['incorrect_password'][lang]}, status=400)

        login(request, user)

        return JsonResponse({'message': 'User is authenticated'})

    @classmethod
    def register(cls, request:HttpRequest, data:Dict[str,Any]):
        error = _check_params(data, name=str, email=str, phone=str, password=str, repeat_password=str)
        if error: return error

        name, email, phone = data['name'], data['email'].lower(), data['phone']
        password, repeat_password = data['password'], data['repeat_password']

        if _is_xss(name) or _is_xss(email):
            return JsonResponse({'error': trsl.AUTH_MSG['invalid_value'][lang]}, status=400)

        lang = get(request.COOKIES, key='lang', default='en')

        if len(name) < 3 or len(name) > 20:
            return JsonResponse({'error': trsl.AUTH_MSG['name_out_of_range'][lang]}, status=400)

        if not cls.__is_valid_email(email):
            return JsonResponse({'error': trsl.AUTH_MSG['incorrect_email'][lang]}, status=400)
        
        if models.User.objects.filter(email=email).exists():
            return JsonResponse({'error': trsl.AUTH_MSG['email_exists'][lang]}, status=400)
        
        if len(phone) < 7 or len(phone) > 12:
            return JsonResponse({'error': trsl.AUTH_MSG['phone_out_of_range'][lang]}, status=400)

        if not phone.isdigit():
            return JsonResponse({'error': trsl.AUTH_MSG['phone_not_digits'][lang]}, status=400)
        
        if len(password) < 7 or len(password) > 100:
            return JsonResponse({'error': trsl.AUTH_MSG['password_out_of_range'][lang]}, status=400)
        
        if password != repeat_password:
            return JsonResponse({'error': trsl.AUTH_MSG['password_mismatch'][lang]}, status=400)

        
        user = models.User(
            email=email,
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.save()
        login(request, user)

        return JsonResponse({'message': 'User is registered'})

    @staticmethod
    def send_code(request:HttpRequest, data:Dict[str,Any]):
        error = _check_params(data, email=str)
        if error: return error

        lang = get(request.COOKIES, key='lang', default='en')
        email = data['email'].lower()

        if not models.User.objects.filter(email=email).exists():
            return JsonResponse({'error': trsl.AUTH_MSG['email_not_found'][lang]}, status=404)

        code = f'{randint(0, 999_999):0>6}'

        try:
            send_mail(
                trsl.AUTH_MSG['recovery_subject'][lang],
                trsl.AUTH_MSG['recovery_message'][lang] + code,
                None, [email]
            )
        except:
            return JsonResponse({'error': trsl.AUTH_MSG['sending_error'][lang]}, status=502)

        cache.set(f'recovery_{email}', (code, 3), 3600)

        return JsonResponse({'message': trsl.AUTH_MSG['code_sent'][lang]})

    @staticmethod
    def change_password(request:HttpRequest, data:Dict[str,Any]):
        error = _check_params(data, email=str, code=str, password=str, repeat_password=str)
        if error: return error

        lang = get(request.COOKIES, key='lang', default='en')
        email, code = data['email'].lower(), data['code']

        try:
            user = models.User.objects.defer().get(email=email)
        except ObjectDoesNotExist:
            return JsonResponse({'error': trsl.AUTH_MSG['email_not_found'][lang]}, status=404)
        
        code_key = f'recovery_{email}'
        if not cache.has_key(code_key):
            return JsonResponse({'error': trsl.AUTH_MSG['code_not_found'][lang]}, status=404)
        
        curr_code, attempts = cache.get(code_key)

        if curr_code != code:
            attempts -= 1
            if attempts > 0:
                cache.set(code_key, (curr_code, attempts))
                return JsonResponse({'error': trsl.AUTH_MSG['incorrect_code'][lang] + str(attempts)}, status=400)
            else:
                cache.delete(code_key)
                return JsonResponse({'error': trsl.AUTH_MSG['request_new_code'][lang]}, status=400)
        
        password, repeat_password = data['password'], data['repeat_password']

        if len(password) < 7 or len(password) > 100:
            return JsonResponse({'error': trsl.AUTH_MSG['password_out_of_range'][lang]}, status=400)
        
        if password != repeat_password:
            return JsonResponse({'error': trsl.AUTH_MSG['password_mismatch'][lang]}, status=400)

        cache.delete(code_key)
        user.set_password(password)
        user.save(update_fields=('password',))
        login(request, user)

        return JsonResponse({'message': 'Password reset'})

class APIUserDataActions(ABC):
    @classmethod
    def change_info(cls, user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, name=str, email=str, phone=str)
        if error: return error
        
        name, email, phone = data['name'], data['email'].lower(), data['phone']

        if _is_xss(name) or _is_xss(email):
            return JsonResponse({'error': trsl.AUTH_MSG['invalid_value'][lang]}, status=400)

        if len(name) < 3 or len(name) > 20:
            return JsonResponse({'error': trsl.AUTH_MSG['name_out_of_range'][lang]}, status=400)

        if not cls.__is_valid_email(email):
            return JsonResponse({'error': trsl.AUTH_MSG['incorrect_email'][lang]}, status=400)

        if models.User.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({'error': trsl.AUTH_MSG['email_exists'][lang]}, status=400)
        
        if len(phone) < 6 or len(phone) > 12 or not phone.isdigit():
            return JsonResponse({'error': trsl.AUTH_MSG['phone_out_of_range'][lang]}, status=400)

        user.name, user.email, user.phone = name, email, phone
        user.save(update_fields=('name', 'email', 'phone'))

        return JsonResponse({'message': trsl.USER_DATA_MSG['info_saved'][lang]})

    @staticmethod
    def change_password(request:HttpRequest, user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, current_password=str, new_password=str, repeat_password=str)
        if error: return error
        
        curr_pass   = data['current_password']
        new_pass    = data['new_password']
        repeat_pass = data['repeat_password']

        if not user.check_password(curr_pass):
            return JsonResponse({'error': trsl.AUTH_MSG['incorrect_password'][lang]}, status=400)

        if len(new_pass) < 6 or len(new_pass) > 100:
            return JsonResponse({'error': trsl.AUTH_MSG['password_out_of_range'][lang]}, status=400)
        
        if new_pass != repeat_pass:
            return JsonResponse({'error': trsl.AUTH_MSG['password_mismatch'][lang]}, status=400)

        user.set_password(new_pass)
        user.save(update_fields=('password',))

        return JsonResponse({'message': trsl.USER_DATA_MSG['password_saved'][lang]})
    
    @staticmethod
    def change_address(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, city=str, street=str, index=str)
        if error: return error
        
        city, street, index = data['city'], data['street'], data['index']

        if _is_xss(city) or _is_xss(street):
            return JsonResponse({'error': trsl.AUTH_MSG['invalid_value'][lang]}, status=400)

        if not city or not street or not index:
            return JsonResponse({'error': trsl.USER_DATA_MSG['is_empty'][lang]}, status=400)

        if city.find(';;') != -1 or street.find(';;') != -1:
            return JsonResponse({'error': trsl.USER_DATA_MSG['invalid_character'][lang]}, status=400)
        
        if len(city) < 3 or len(street) < 3:
            return JsonResponse({'error': trsl.USER_DATA_MSG['city_street_out_of_range'][lang]}, status=400)
        
        if not index.isdigit():
            return JsonResponse({'error': trsl.USER_DATA_MSG['index_not_digits'][lang]}, status=400)
        
        address = ';;'.join((city, street, index))

        if len(address) > 150:
            return JsonResponse({'error': trsl.USER_DATA_MSG['address_out_of_range'][lang]}, status=400)

        user.address = address
        user.save(update_fields=('address',))

        return JsonResponse({'message': trsl.USER_DATA_MSG['address_saved'][lang]})

class APIProductActions(ABC):
    @staticmethod
    def favorite_add(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, product_id=int)
        if error: return error
        
        try:
            product = models.Product.objects.defer().get(id=data['product_id'])
            user.favorites.add(product)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        return JsonResponse({
            'message': trsl.PRODUCTS_MSG['favorites_add'][lang],
            'count': user.favorites.count(),
        })

    @staticmethod
    def favorite_remove(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, ids=list)
        if error: return error

        for i in data['ids']:
            if not isinstance(i, int):
                return JsonResponse({'error': f'Incorret type of parameter "ids"'}, status=400)

        products = user.favorites.filter(id__in=data['ids'])
        delete_count = products.count()
        user.favorites.remove(*products)
        
        return JsonResponse({
            'message': str(delete_count) + trsl.PRODUCTS_MSG['favorites_remove'][lang],
            'count': user.favorites.count(),
        })

    @staticmethod
    def cart_add(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, product_id=int, color=str, quantity=int)
        if error: return error

        try:
            product = models.Product.objects.only('quantity').get(id=data['product_id'])
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        if data['color'] == 'null':
            data['color'] = product.characteristic.get_first_color()
        elif not data['color'] in product.characteristic.get_colors():
            return JsonResponse({'error': 'Incorret parameter "color"'}, status=400)

        if data['quantity'] < 1 or data['quantity'] > product.quantity:
            return JsonResponse({'error': 'Incorret parameter "quantity"'}, status=400)

        models.CartProduct.objects.create(
            user=user,
            product=product,
            color=data['color'],
            quantity=data['quantity'],
            datetime=datetime.now(),
        )

        return JsonResponse({
            'message': trsl.PRODUCTS_MSG['cart_add'][lang],
            'count': user.cart_products.count(),
        })

    @staticmethod
    def cart_remove(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, ids=list)
        if error: return error

        for i in data['ids']:
            if not isinstance(i, int):
                return JsonResponse({'error': f'Incorret type of parameter "ids"'}, status=400)

        delete_log = models.CartProduct.objects.filter(id__in=data['ids']).delete()
        
        return JsonResponse({
            'message': str(delete_log[0]) + trsl.PRODUCTS_MSG['cart_remove'][lang],
            'count': user.cart_products.count(),
        })

    @staticmethod
    def cart_quantity(user:models.User, data:Dict[str,Any]):
        error = _check_params(data, cart_product_id=int, value=int)
        if error: return error
        
        try:
            cart_product = models.CartProduct.objects.select_related('product').only(
                'product__quantity'
            ).get(id=data['cart_product_id'])
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Cart product not found'}, status=404)
        
        if data['value'] < 1 or data['value'] > cart_product.product.quantity:
            return JsonResponse({'error': 'Incorret parameter "value"'}, status=400)
        
        cart_product.quantity = data['value'];
        cart_product.save(update_fields=('quantity',))

        return JsonResponse({'message': 'Quantity is update'})

    @staticmethod
    def order_add(user:models.User, data:Dict[str,Any], lang:str):
        if not user.address:
            return JsonResponse({'error': f'Indicate your delivery address'}, status=401)

        error = _check_params(data, color=str, quantity=int)
        if error: return error

        if 'cart_product_id' in data:
            if not isinstance(data['cart_product_id'], int):
                return JsonResponse({'error': f'Incorret type of parameter "cart_product_id"'}, status=400)
            
            try:
                cart_product = models.CartProduct.objects.select_related('product').only(
                    'product__price', 'product__discount', 'product__quantity'
                ).get(id=data['cart_product_id'])
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Cart product not found'}, status=404)
            
            product = cart_product.product
        
        elif 'product_id' in data:
            if not isinstance(data['product_id'], int):
                return JsonResponse({'error': f'Incorret type of parameter "product_id"'}, status=400)
            
            try:
                product = models.Product.objects.only('price', 'discount', 'quantity').get(id=data['product_id'])
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
        else:
            return JsonResponse({'error': f'Parameters "cart_product_id" or "product_id" not found'}, status=400)


        if not data['color'] in product.characteristic.get_colors():
            return JsonResponse({'error': 'Incorret parameter "color"'}, status=400)

        if data['quantity'] < 1 or data['quantity'] > product.quantity:
            return JsonResponse({'error': 'Incorret parameter "quantity"'}, status=400)


        models.Order.objects.create(
            user=user,
            product=product,
            product_price=product.price - product.price * product.discount,
            color=data['color'],
            quantity=data['quantity'],
            datetime=datetime.now(),
            status='is confirmed',
        )

        response = {
            'message': trsl.PRODUCTS_MSG['orders_add'][lang],
            'count': user.orders.count(),
        }

        if 'cart_product_id' in data:
            cart_product.delete()
            response['cart_count'] = user.cart_products.count()
        
        return JsonResponse(response)

    @staticmethod
    def order_cancel(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, ids=list)
        if error: return error

        for i in data['ids']:
            if not isinstance(i, int):
                return JsonResponse({'error': f'Incorret type of parameter "ids"'}, status=400)

        update_log = models.Order.objects.filter(id__in=data['ids'], status='is confirmed').update(status='canceled')

        return JsonResponse({
            'message': str(update_log) + trsl.PRODUCTS_MSG['orders_cancel'][lang],
            'new_status': trsl.ORDER_STATUS['canceled'][lang],
            'new_status_color': models.Order.STATUS_COLORS['canceled'],
            'count': user.orders.count(),
        })

    @staticmethod
    def order_remove(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, ids=list)
        if error: return error

        for i in data['ids']:
            if not isinstance(i, int):
                return JsonResponse({'error': f'Incorret type of parameter "ids"'}, status=400)

        delete_log = models.Order.objects.filter(id__in=data['ids'], status__in=['canceled', 'arrived']).delete()

        return JsonResponse({
            'message': str(delete_log[0]) + trsl.PRODUCTS_MSG['orders_remove'][lang],
            'count': user.orders.count(),
        })

    @staticmethod
    def browsed_remove(user:models.User, data:Dict[str,Any], lang:str):
        error = _check_params(data, ids=list)
        if error: return error
        
        for i in data['ids']:
            if not isinstance(i, int):
                return JsonResponse({'error': f'Incorret type of parameter "ids"'}, status=400)

        delete_log = models.BrowsedProduct.objects.filter(id__in=data['ids']).delete()

        return JsonResponse({
            'message': str(delete_log[0]) + trsl.PRODUCTS_MSG['browsed_remove'][lang],
            'count': user.browsed_products.count(),
        })
