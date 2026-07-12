from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    def product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    product_count.short_description = 'Количество товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'in_stock_display', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock', 'is_active']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'description')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'stock')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Дата', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def in_stock_display(self, obj):
        return 'В наличии' if obj.in_stock else 'Нет в наличии'
    in_stock_display.short_description = 'Наличие'
