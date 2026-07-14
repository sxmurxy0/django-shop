from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Order, OrderItem, OrderStatus
from cart.cart import CartManager


@login_required
def order_create(request):
    cart_manager = CartManager(request)
    cart_items = cart_manager.get_items()
    
    if not cart_items:
        messages.error(request, 'Корзина пуста. Добавьте товары перед оформлением заказа.')
        return redirect('cart:detail')
    
    if request.method == 'POST':
        user = request.user
        
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request, 
                    f'Товара "{item.product.name}" недостаточно на складе. Доступно: {item.product.stock} шт.'
                )
                return redirect('cart:detail')
        
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                total_price=cart_manager.get_total_price(),
                postal_code=request.POST.get('postal_code', ''),
                email=request.POST.get('email', user.email),
                comment=request.POST.get('comment', '')
            )
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price
                )
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            cart_manager.clear()
        
        messages.success(request, f'Заказ #{order.id} успешно оформлен!')
        return redirect('order:order_detail', order_id=order.id)
    
    user = request.user
    context = {
        'cart_items': cart_items,
        'total_price': cart_manager.get_total_price(),
        'user': user,
    }
    return render(request, 'order_create.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'status_choices': OrderStatus.choices,
    }
    return render(request, 'order_detail.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    
    return render(request, 'order_list.html', context)

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == OrderStatus.NEW:
        with transaction.atomic():
            order.status = OrderStatus.CANCELLED
            order.save()
            
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
        
        messages.success(request, f'Заказ #{order.id} отменен.')
    else:
        messages.error(request, 'Невозможно отменить заказ в текущем статусе.')
    
    return redirect('order:order_detail', order_id=order.id)