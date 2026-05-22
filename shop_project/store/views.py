from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category

# Старые страницы из начала лабораторной
def about_author(request):
    return HttpResponse("<h1>Информация об авторе</h1><p>Привет! Я автор этого проекта.</p>")

def about_lab(request):
    return HttpResponse("<h1>О лаборатории</h1>")

# Список товаров с поиском, фильтрацией и сортировкой
def product_list(request):
    products = Product.objects.all()
    
    # Поиск по названию
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(title__icontains=search_query)
        
    # Фильтрация по категории
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    # Сортировка по цене
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    categories = Category.objects.all()
    
    return render(request, 'store/product_list.html', {
        'products': products, 
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_sort': sort_by
    })

# Страница отдельного товара
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})
