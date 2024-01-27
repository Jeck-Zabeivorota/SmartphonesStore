from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('Products', views.products, name='products'),
    path('FAQ', views.faq, name='faq'),
    path('Product', views.product, name='product'),
    path('Account/Info', views.user_info, name='user_info'),
    path('Account/Cart', views.cart, name='cart'),
    path('Account/Orders', views.orders, name='orders'),
    path('Account/Favorites', views.favorites, name='favorites'),
    path('Account/BrowsedProducts', views.browsed_products, name='browsed_products'),
    path('Account/Authorization', views.auth, name='auth'),
    path('Account/Logout', views.auth_logout, name='auth_logout'),
    path('API/Authorization', views.api_auth, name='api_auth'),
    path('API/Product', views.api_product, name='api_product'),
    path('API/Products', views.api_products, name='api_products'),
    path('API/Feedback', views.api_feedback, name='api_feedback'),
    path('API/UserData', views.api_user_data, name='api_user_data'),
    path('API/Lang', views.api_lang, name='api_lang'),
]