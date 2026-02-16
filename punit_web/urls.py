from django.urls import path
from . import views
from punit_web.views import login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('order/', views.order, name='order'),
    path('about/', views.about, name='about'),

    path('login/', login_view, name='login'),  # ✅ Only ONE login

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order-success'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),

    path('search/', views.search_products, name='search'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
