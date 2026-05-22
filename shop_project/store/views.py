from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Manufacturer, Cart, CartItem

# 1. Список товаров (Каталог)
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all()

    # Поиск по названию ИЛИ описанию (используем Q-объекты)
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Фильтрация по категории
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    # Фильтрация по производителю
    manufacturer_id = request.GET.get('manufacturer', '')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_manufacturer': manufacturer_id,
    })

# 2. Детальная информация о товаре
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

# 3. Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        if cart_item.quantity + 1 <= product.stock_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Количество товара {product.title} увеличено.")
        else:
            messages.error(request, "Недостаточно товара на складе.")
    else:
        messages.success(request, f"Товар {product.title} добавлен в корзину.")
        
    return redirect('product_list')

# 4. Обновление количества товара в корзине
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        
        if new_quantity <= cart_item.product.stock_quantity:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, "Количество обновлено.")
        else:
            messages.error(request, f"На складе доступно только {cart_item.product.stock_quantity} шт.")
            
    return redirect('cart_view')

# 5. Удаление товара из корзины
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Товар удален из корзины.")
    return redirect('cart_view')

# 6. Просмотр корзины
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart.html', {'cart': cart})
