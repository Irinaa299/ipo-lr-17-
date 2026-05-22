import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Manufacturer, Category, Product, Cart, CartItem

class Command(BaseCommand):
    help = 'Заполняет базу данных спортивными аксессуарами для подростков'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очистка старых данных электроники...')
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Manufacturer.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Создание спортивных брендов...')
        manufacturers = []
        brand_data = [
            ('Nike', 'США'), ('Adidas', 'Германия'), 
            ('Puma', 'Германия'), ('Under Armour', 'США'), ('Reebok', 'США')
        ]
        for name, country in brand_data:
            m = Manufacturer.objects.create(
                name=name,
                country=country,
                description=f'Спортивные товары и аксессуары от всемирного бренда {name}.'
            )
            manufacturers.append(m)

        self.stdout.write('Создание категорий спортивных аксессуаров...')
        categories = []
        category_names = [
            'Спортивные рюкзаки', 'Бутылки для воды', 'Фитнес-браслеты', 
            'Напульсники и повязки', 'Спортивные сумки'
        ]
        for name in category_names:
            c = Category.objects.create(
                name=name,
                description=f'Стильные и надежные {name.lower()} для активных подростков.'
            )
            categories.append(c)

        self.stdout.write('Создание спортивных товаров (34 шт)...')
        products = []
        
        # Списки для генерации реалистичных названий
        backpack_titles = ['Рюкзак городской Youth', 'Рюкзак влагозащитный Neo', 'Рюкзак для тренировок Sport', 'Школьный спорт-рюкзак Teen']
        bottle_titles = ['Бутылка матовая Шейкер', 'Спортивная бутылка фляга', 'Термобутылка для тренировок', 'Бутылка соломка Active']
        bracelet_titles = ['Фитнес-браслет Smart Band', 'Спортивный трекер пульса', 'Силиконовый браслет Run', 'Браслет с шагомером']

        for i in range(1, 35):
            category = random.choice(categories)
            brand = random.choice(manufacturers)
            
            # Подбираем логичное название в зависимости от выбранной категории
            if category.name == 'Спортивные рюкзаки':
                title = f"{random.choice(backpack_titles)} {brand.name} #{i}"
            elif category.name == 'Бутылки для воды':
                title = f"{random.choice(bottle_titles)} {brand.name} #{i}"
            elif category.name == 'Фитнес-браслеты':
                title = f"{random.choice(bracelet_titles)} #{i}"
            else:
                title = f"Спортивный аксессуар Active #{i}"

            p = Product.objects.create(
                title=title,
                description=f'Идеальный выбор для подростков. Качественные материалы, яркий молодежный дизайн, высокая прочность для активного отдыха и занятий спортом.',
                price=random.randint(15, 120) + 0.90,  # Цены на аксессуары в рублях/у.е.
                stock_quantity=random.randint(5, 40),
                category=category,
                manufacturer=brand
            )
            products.append(p)

        self.stdout.write('Создание тестовых пользователей и корзин...')
        for i in range(1, 6):
            username = f'teen_user_{i}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@sport.com',
                password='password123'
            )
            cart = Cart.objects.create(user=user)
            selected_products = random.sample(products, 2)
            for product in selected_products:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=random.randint(1, 2)
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно переведена на спортивные аксессуары!'))
