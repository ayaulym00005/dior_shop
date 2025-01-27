from django.contrib import admin
from .models import Product, Cart

# Создаём класс для настройки отображения модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']  # Настроить поля, которые будут отображаться в списке

# Регистрируем модель и её настройки
admin.site.register(Product, ProductAdmin)

# Регистрируем модель Cart без дополнительных настроек
admin.site.register(Cart)

