# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('catalog/', views.catalog, name='catalog'),
    path('basket/', views.basket, name='basket'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
