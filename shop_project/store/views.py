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
import io
import openpyxl
from django.core.mail import EmailMessage

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    # Если в корзине пусто, не пускаем дальше
    if not cart_items:
        messages.error(request, "Ваша корзина пуста. Оформление невозможно.")
        return redirect('cart_view')

    # Если пользователь зашел первый раз — открываем форму ввода адреса
    if request.method != 'POST':
        return render(request, 'shop/checkout.html')

    # Если пользователь отправил форму (POST-запрос):
    # Принимаем данные, введенные пользователем
    user_address = request.POST.get('address', '')
    user_comment = request.POST.get('comment', 'Без комментария')

    # Создаем Excel книгу в памяти для чека
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Чек заказа"

    # Заполняем накладную текстовыми пояснениями
    ws['A1'] = "ЭЛЕКТРОННЫЙ ЧЕК СПОРТИВНОГО МАГАЗИНА"
    ws['A2'] = f"Покупатель (User): {request.user.username}"
    ws['A3'] = f"Адрес доставки: {user_address}"
    ws['A4'] = f"Комментарий: {user_comment}"
    ws['A5'] = "--------------------------------------------------"

    # Шапка таблицы
    ws.append(["Наименование товара", "Количество", "Цена за шт.", "Итоговая стоимость"])

    total_price = 0
    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total

        # Добавляем строку товара в Excel
        ws.append([item.product.title, item.quantity, float(item.product.price), float(item_total)])

        # Списываем купленное количество со склада
        item.product.stock_quantity -= item.quantity
        item.product.save()

    ws.append([])
    ws.append(["ОБЩАЯ СУММА К ОПЛАТЕ:", "", "", float(total_price)])

    # Сохраняем сгенерированный Excel в байтовый поток памяти для отправки по почте
    excel_file = io.BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    # Формируем и отправляем Email с вложением чека (Задание 4)
    user_email = request.user.email if request.user.email else f"{request.user.username}@example.com"

    subject = f"Ваш чек заказа в магазине Спортивных товаров #{cart.id}"
    body = (
        f"Здравствуйте, {request.user.username}!\n\n"
        f"Ваш заказ успешно сформирован и передан в курьерскую службу.\n"
        f"Пояснение к вашим данным:\n"
        f"- Адрес доставки: {user_address}\n"
        f"- Комментарий: {user_comment}\n"
        f"- Итого к оплате: {total_price} руб.\n\n"
        f"Подробный электронный чек находится во вложении (формат Excel).\n"
        f"Спасибо за покупку!"
    )

    email = EmailMessage(
        subject,
        body,
        'shop@sport-accessories.com',
        [user_email]
    )

    # Прикрепляем созданный Excel файл к письму
    email.attach('sport_order_check.xlsx', excel_file.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()

    # Очищаем корзину пользователя после успешного оформления
    cart_items.delete()

    # Выводим результаты обработки на экран с подробными пояснениями для ЛР
    return HttpResponse(
        f"<body style='font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; max-width: 600px; background: #fafafa;'>"
        f"<div style='background: #fff; padding: 30px; border: 2px solid #28a745; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>"
        f"<h2 style='color: #28a745; margin-top: 0;'>🎉 Заказ успешно завершен!</h2>"
        f"<p><b>Пояснение выводимых результатов обработки вашей формы:</b></p>"
        f"<ul>"
        f"<li><b>Статус отправки:</b> Чек успешно сформирован в Excel и отправлен на ваш email: <u>{user_email}</u></li>"
        f"<li><b>Указанный адрес доставки:</b> {user_address}</li>"
        f"<li><b>Ваш комментарий:</b> {user_comment}</li>"
        f"<li><b>Итоговая стоимость:</b> <b style='color: #e44d26;'>{total_price} руб.</b></li>"
        f"<li><b>Состояние корзины:</b> Корзина полностью очищена.</li>"
        f"</ul>"
        f"<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0 Triton;'>"
        f"<a href='/catalog/' style='display: inline-block; background: #007bff; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; font-weight: bold;'>Вернуться в каталог товаров</a>"
        f"</div>"
        f"</body>"
    )
