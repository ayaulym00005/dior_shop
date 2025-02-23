from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Product, Cart  # CartItem на Cart
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from .models import Category
from .models import Product
import json
import random
from django.contrib import messages
from accounts.models import CustomUser
from .forms import RegistrationForm
from .utils import send_sms_via_email  # Функция для отправки SMS

def generate_verification_code():
    return str(random.randint(100000, 999999))  # Генерация случайного 6-значного кода

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            phone_number = form.cleaned_data.get('phone_number')
            verification_code = generate_verification_code()
            user.verification_code = verification_code  # Сохраняем код в базе данных
            user.save()

            # Отправляем SMS с кодом
            send_sms_via_email(phone_number, f'Ваш код подтверждения: {verification_code}')  # Обновленный вызов

            # Отправляем письмо для подтверждения регистрации
            messages.success(request, 'Пожалуйста, проверьте вашу почту для подтверждения.')
            return redirect('verify')  # Перенаправление на страницу для ввода кода
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})



class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_products'] = Product.objects.filter(is_popular=True)[:6]  # Берём 6 товаров
        return context

def home(request):
    return render(request, 'store/index.html')  # Путь к шаблону


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Неверное имя пользователя или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def catalog(request):
    products = Product.objects.all()
    return render(request, 'store/catalog.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({'message': f'{product.name} добавлен в корзину!'}, status=200)
    else:
        return JsonResponse({'message': 'Для добавления товара в корзину нужно войти в систему.'}, status=400)

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart')

def basket(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/basket.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def profile(request):
    user = request.user
    return render(request, 'store/profile.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'store/update_profile.html', {'form': form})

def verify(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        phone_number = request.POST.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.verification_code == verification_code:
                user.is_verified = True  # Помечаем как подтвержденного
                user.save()
                messages.success(request, 'Ваша регистрация успешно завершена!')
                return redirect('login')
            else:
                messages.error(request, 'Неверный код подтверждения.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Пользователь с таким номером не найден.')
    return render(request, 'accounts/verify.html')

@login_required
def account(request):
    return render(request, 'accounts/account.html', {'user': request.user})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)  # Получаем товар по id
    return render(request, 'store/product_detail.html', {'product': product})