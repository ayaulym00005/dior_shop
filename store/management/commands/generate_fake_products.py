from django.core.management.base import BaseCommand
from store.models import Product, Category
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate 100 fake products'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Получим все существующие категории
        categories = Category.objects.all()
        
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Please add categories first.'))
            return

        for _ in range(100):
            name = fake.company()  # Генерация случайного имени товара (можно изменить на word, если нужно)
            description = fake.text()  # Генерация случайного описания
            price = round(random.uniform(10.0, 100.0), 2)  # Генерация случайной цены от 10 до 100
            image = 'product_images/default.jpg'  # Путь к изображению, можно заменить

            # Случайный выбор категории
            category = random.choice(categories)

            Product.objects.create(
                name=name,
                description=description,
                price=price,
                image=image,
                category=category
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 100 fake products'))
