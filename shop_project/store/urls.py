from django.urls import path
from . import views

urlpatterns = [
    # Каталог и товары
    path('', views.product_list, name='product_list'), # Оставляем главную для удобства проверки
    path('catalog/', views.product_list, name='catalog_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Корзина (Задание 1)
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
