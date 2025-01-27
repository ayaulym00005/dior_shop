from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Product, Cart  # Исправил CartItem на Cart
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'store/home.html')

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация сразу после регистрации
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})


# Вход пользователя
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
    products = Product.objects.all()  # Получаем все продукты
    
    return render(request, 'store/catalog.html', {'products': products})

# Страница About Us
def about(request):
    return render(request, 'store/about.html')

# Страница Contact
def contact(request):
    return render(request, 'store/contact.html')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        # Проверяем, есть ли уже товар в корзине для этого пользователя
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            # Если товар уже есть в корзине, увеличиваем количество
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({'message': f'{product.name} добавлен в корзину!'}, status=200)
    else:
        return JsonResponse({'message': 'Для добавления товара в корзину нужно войти в систему.'}, status=400)



def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Направление на страницу входа
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
    except Cart.DoesNotExist:
        # Если товар не найден в корзине пользователя
        pass
    return redirect('cart')


def basket(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправление на страницу входа, если пользователь не авторизован

    # Получаем все товары в корзине текущего пользователя
    cart_items = Cart.objects.filter(user=request.user)

    # Вычисляем общую стоимость
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Передаем данные в шаблон
    return render(request, 'store/basket.html', {'cart_items': cart_items, 'total_price': total_price})
