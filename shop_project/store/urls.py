from django.urls import path
from . import views

urlpatterns = [
    # Каталог товаров (будет открываться и на главной, и по адресу /catalog/)
    path('', views.product_list, name='product_list'),
    path('catalog/', views.product_list, name='catalog_list'),
    
    # Карточка одного товара
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Функционал корзины
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),

    # Страница оформления заказа для 19-й ЛР
    path('checkout/', views.checkout, name='checkout'),
]
