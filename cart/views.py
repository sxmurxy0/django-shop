from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from shop.models import Product
from .cart import CartManager


@login_required
def cart_detail(request):
    cart_manager = CartManager(request)
    items = cart_manager.get_items()
    total_price = cart_manager.get_total_price()
    total_quantity = cart_manager.get_total_quantity()
    
    context = {
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    }
    return render(request, 'detail.html', context)

@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        messages.error(request, 'Количество должно быть больше 0')
        return redirect('cart:detail')
    
    if quantity > product.stock:
        messages.error(request, f'На складе только {product.stock} шт.')
        return redirect('cart:detail')
    
    cart_manager = CartManager(request)
    cart_item = cart_manager.add(product_id, quantity)
    
    if cart_item:
        messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
    else:
        messages.error(request, 'Не удалось добавить товар в корзину.')
    
    return redirect('cart:detail')

@login_required
@require_POST
def cart_update(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 0:
        messages.error(request, 'Количество должно быть больше 0')
        return redirect('cart:detail')
    
    cart_manager = CartManager(request)
    
    if quantity == 0:
        cart_manager.remove(product_id)
        messages.info(request, 'Товар удален из корзины')
    else:
        cart_item = cart_manager.update_quantity(product_id, quantity)
        if cart_item:
            messages.success(request, 'Количество обновлено')
        else:
            messages.error(request, 'Товар не найден в корзине')
    
    return redirect('cart:detail')

@login_required
def cart_remove(request, product_id):
    cart_manager = CartManager(request)
    product = get_object_or_404(Product, id=product_id)
    cart_manager.remove(product_id)
    messages.success(request, f'Товар "{product.name}" удален из корзины.')
    return redirect('cart:detail')

@login_required
def cart_clear(request):
    cart_manager = CartManager(request)
    cart_manager.clear()
    messages.info(request, 'Корзина очищена.')
    return redirect('cart:detail')

@login_required
def cart_count(request):
    cart_manager = CartManager(request)
    return JsonResponse({'count': cart_manager.get_total_quantity()})
