from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    
    # Каталог товаров
    path('catalog/', views.product_list, name='product_list'),
    
    # Карточка одного товара
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Функционал корзины
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),

    # Страница оформления заказа
    path('checkout/', views.checkout, name='checkout'),
]