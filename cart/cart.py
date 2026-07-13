from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from shop.models import Product


class CartManager:
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None

    def get_cart(self):
        if self.user:
            cart, created = Cart.objects.get_or_create(user=self.user)
            return cart
        return None

    def add(self, product_id, quantity=1):
        if not self.user:
            return None
        
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart()
        
        if not product.in_stock:
            return None
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': product.price}
        )
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        return cart_item

    def remove(self, product_id):
        cart = self.get_cart()
        if cart:
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    def update_quantity(self, product_id, quantity):
        cart = self.get_cart()
        if cart and quantity > 0:
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                if quantity > cart_item.product.stock:
                    quantity = cart_item.product.stock
                cart_item.quantity = quantity
                cart_item.save()
                return cart_item
        return None

    def clear(self):
        cart = self.get_cart()
        if cart:
            cart.clear()

    def get_items(self):
        cart = self.get_cart()
        if cart:
            return cart.items.select_related('product').all()
        return []

    def get_total_price(self):
        cart = self.get_cart()
        if cart:
            return cart.get_total_price()
        return 0

    def get_total_quantity(self):
        cart = self.get_cart()
        if cart:
            return cart.get_total_quantity()
        return 0

    def get_cart_id(self):
        cart = self.get_cart()
        return cart.id if cart else None