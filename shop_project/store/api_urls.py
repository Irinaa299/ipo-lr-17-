from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ManufacturerViewSet, CategoryViewSet, ProductViewSet,
    CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet
)

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]