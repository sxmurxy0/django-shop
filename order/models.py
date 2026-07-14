from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from shop.models import Product


class OrderStatus(models.TextChoices):
    NEW = 'new', _('Новый')
    PROCESSING = 'processing', _('Собирается на складе')
    SHIPPED = 'shipped', _('Передан службе доставки')
    DELIVERED = 'delivered', _('Доставлен')
    CANCELLED = 'cancelled', _('Отменён')

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('Пользователь')
    )
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )
    total_price = models.DecimalField(_('Итоговая сумма'), max_digits=10, decimal_places=2, default=0)
    
    postal_code = models.CharField(_('Почтовый индекс'), max_length=20, blank=True)
    email = models.EmailField(_('Email'))
    
    comment = models.TextField(_('Комментарий к заказу'), blank=True)
    
    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.user.username}'

    def get_status_display_ru(self):
        return dict(OrderStatus.choices).get(self.status, self.status)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Заказ')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('Товар')
    )
    quantity = models.PositiveIntegerField(_('Количество'), default=1)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Товар в заказе')
        verbose_name_plural = _('Товары в заказе')

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        if self.quantity is not None and self.price is not None:
             return self.price * self.quantity
        return 0