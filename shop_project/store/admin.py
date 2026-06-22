

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Manufacturer, Cart, CartItem, Order, OrderItem, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'delivery_city', 'favorite_category')
    search_fields = ('user__username', 'full_name', 'phone')
    list_filter = ('delivery_city', 'favorite_category')