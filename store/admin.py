from django.contrib import admin
from .models import Product, Cart

# Создаём класс для настройки отображения модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_category')

    def get_category(self, obj):
        return obj.category.name  # Adjust this according to your actual model relationship
    get_category.admin_order_field = 'category'  # Allows sorting by category
    get_category.short_description = 'Category'


# Регистрируем модель и её настройки
admin.site.register(Product, ProductAdmin)

# Регистрируем модель Cart без дополнительных настроек
admin.site.register(Cart)

