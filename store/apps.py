# store/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        from .models import Product  # Переместил импорт сюда
        post_migrate.connect(create_initial_products, sender=self)

def create_initial_products(sender, **kwargs):
    # Создание данных после миграции
    from .models import Product  # Импортируем модели тут, чтобы избежать ошибок
    if not Product.objects.exists():
        Product.objects.create(
            name="Пример продукта",
            description="Описание продукта",
            price=100.00,
            image="path_to_image.jpg"  # Путь к изображению
        )
