import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from store.models import Category, Manufacturer, Product

# Создаём категории
cat1 = Category.objects.get_or_create(name='Спортивные рюкзаки')[0]
cat2 = Category.objects.get_or_create(name='Бутылки для воды')[0]
cat3 = Category.objects.get_or_create(name='Фитнес-браслеты')[0]

# Создаём производителей
mfr1 = Manufacturer.objects.get_or_create(name='Nike')[0]
mfr2 = Manufacturer.objects.get_or_create(name='Adidas')[0]
mfr3 = Manufacturer.objects.get_or_create(name='Puma')[0]

# Создаём товары
products = [
    {'title': 'Рюкзак Nike Sport', 'desc': 'Удобный спортивный рюкзак', 'price': 2500, 'stock': 10, 'cat': cat1, 'mfr': mfr1},
    {'title': 'Рюкзак Adidas Pro', 'desc': 'Профессиональный рюкзак', 'price': 3200, 'stock': 5, 'cat': cat1, 'mfr': mfr2},
    {'title': 'Бутылка Nike 1L', 'desc': 'Спортивная бутылка для воды', 'price': 800, 'stock': 20, 'cat': cat2, 'mfr': mfr1},
    {'title': 'Фитнес-браслет Puma', 'desc': 'Трекер активности', 'price': 4500, 'stock': 8, 'cat': cat3, 'mfr': mfr3},
    {'title': 'Бутылка Adidas 0.5L', 'desc': 'Компактная бутылка', 'price': 600, 'stock': 15, 'cat': cat2, 'mfr': mfr2},
]

for p in products:
    Product.objects.get_or_create(
        title=p['title'],
        defaults={
            'description': p['desc'],
            'price': p['price'],
            'stock_quantity': p['stock'],
            'category': p['cat'],
            'manufacturer': p['mfr'],
        }
    )

print("✅ Готово! Добавлено 3 категории, 3 производителя и 5 товаров")