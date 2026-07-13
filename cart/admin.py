from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_total_quantity', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'price', 'get_total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['created_at']
