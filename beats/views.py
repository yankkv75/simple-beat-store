from django.shortcuts import render, get_object_or_404

from .forms import SignUpForm
from .models import Category, Beat, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


def home(request, category_slug=None):
    """Домашняя страница"""
    category_page = None
    beats = None
    if category_slug is not None:
        category_page = get_object_or_404(Category, slug=category_slug)
        beats = Beat.objects.filter(category=category_page)
    else:
        beats = Beat.objects.all().filter()

    return render(request, 'home.html', {'category': category_page, 'beats': beats})


def beat(request, category_slug, beat_slug):
    try:
        beat = Beat.objects.get(category__slug=category_slug, slug=beat_slug)
    except Exception as e:
        raise e
    return render(request, 'beat.html', {'beat': beat})


def _cart_id(request):
    """Сохранение или создание корзины по время сессии"""
    cart = request.session.session_key  # Сохранение корзины во время сессии фреймворку 'session'
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, beat_id):
    """Добавление товара и обновление кол-ва в корзине"""
    beat = Beat.objects.get(id=beat_id)
    try:  # Получение корзины из текущей сессии вызовом в методе get _cart_id метод
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:  # Если корзины не существует, то создаем ее
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(beat=beat, cart=cart)
        # Условие при котром из описания товара нельзя было добавить товар в корзину
        if cart_item.quantity < cart_item.beat.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(beat=beat,
                                            quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    """Функция для вывода информации в корзине"""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Получение cart_item из текущей сессии
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.beat.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def sign_up_view(request):
    """Форма регистрации"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def sign_in_view(request):
    """Форма входа в аккаунт"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


def sign_out(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('signin')