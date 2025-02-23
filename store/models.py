from django.db import models
from django.conf import settings  # Для использования кастомного пользователя

class Category(models.Model):
    """Модель для хранения категорий продуктов"""
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Модель для корзины покупок пользователя"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts", verbose_name="User")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="carts", verbose_name="Product")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
