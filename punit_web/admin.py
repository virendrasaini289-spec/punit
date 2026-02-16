from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product
from .models import Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('title',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone','address' ,'city', 'payment_method', 'total_price', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('name', 'email', 'phone')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)

from .models import Customer

admin.site.register(Customer)