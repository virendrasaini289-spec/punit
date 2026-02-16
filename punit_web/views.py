# =========================================
# DJANGO IMPORTS
# =========================================
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

# =========================================
# MODELS IMPORT
# =========================================
from .models import (
    Product,
    Category,
    Cart,
    Order,
    OrderItem,
    Customer,
    UserProfile
)

from .forms import CustomerRegisterForm


# =========================================
# HOME PAGE
# =========================================
def home(request):
    products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'store/home.html', {'products': products})


# =========================================
# MENU PAGE
# =========================================
def menu(request):
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories
    }

    return render(request, "store/menu.html", context)


# =========================================
# STATIC PAGES
# =========================================
def about(request):
    products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'store/about.html', {'products': products})


def order(request):
    products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'store/orders.html', {'products': products})


def login_page(request):
    products = Product.objects.filter(is_available=True)[:8]
    return render(request, 'store/login.html', {'products': products})


# =========================================
# PRODUCT DETAIL
# =========================================
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


# =========================================
# CART SECTION
# =========================================
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
    else:
        quantity = 1

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, id):
    Cart.objects.filter(id=id, user=request.user).delete()
    return redirect('cart')


# =========================================
# CHECKOUT PAGE
# =========================================
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total_price': total
    }

    return render(request, 'store/checkout.html', context)


# =========================================
# PLACE ORDER (FINAL VERSION - ACTIVE)
# =========================================
def place_order(request):
    if request.method == "POST":
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items:
            return redirect('cart')

        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity

        order = Order.objects.create(
            user=request.user,
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            payment_method=request.POST.get("payment_method"),
            total_price=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return redirect("order-success")


# =========================================
# ORDER SUCCESS PAGE
# =========================================
def order_success(request):
    return render(request, "store/order-success.html")


# =========================================
# SEARCH PRODUCTS
# =========================================
def search_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        products = Product.objects.all()

    return render(request, "store/search.html", {"products": products})


# =========================================
# USER REGISTRATION (CUSTOMER FORM)
# =========================================
def register(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = CustomerRegisterForm()

    return render(request, "store/register.html", {"form": form})


# =========================================
# LOGIN VIEW
# =========================================
def login_view(request):

    
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        
        if request.user.is_authenticated:
         return redirect('home')

    return render(request, "store/login.html")

#================================================
#profile view
#+====================================
@login_required
def profile(request):
    return render(request, "store/profile.html")