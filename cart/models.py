from django.db import models
from django.conf import settings
from shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-created_at']

    def __str__(self):
        return f'Корзина {self.user.username}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = [['cart', 'product']]

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
