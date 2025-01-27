from django.db import models
from django.contrib.auth.models import User  # Импорт User дұрыс жерде болуы керек

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('palette', 'Палетка'),
        ('lipstick', 'Помада'),
        ('highlighter', 'Хайлайтер'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='media/products/')  # Один путь для изображений
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='palette')

    def __str__(self):
        return self.name

class Cart(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
