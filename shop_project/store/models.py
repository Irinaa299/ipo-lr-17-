from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# 4. Модель "Корзина"
class Cart(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='cart', 
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    @property
    def total_price(self):
        """Вычисляет общую стоимость всех элементов в корзине"""
        return sum(item.item_total for item in self.items.all())


# 5. Модель "Элемент корзины"
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='cart_items', 
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product.title} ({self.quantity} шт.)"

    @property
    def item_total(self):
        """Возвращает стоимость данного элемента (цена товара * количество)"""
        return self.product.price * self.quantity

    def clean(self):
        """Валидация: количество товара не должно превышать остаток на складе"""
        super().clean()
        if self.product and self.quantity > self.product.stock_quantity:
            raise ValidationError({
                'quantity': f"Невозможно добавить {self.quantity} шт. На складе осталось всего {self.product.stock_quantity} шт."
            })

    def save(self, *args, **kwargs):
        """Вызываем валидацию перед каждым сохранением в БД"""
        self.full_clean()
        super().save(*args, **kwargs)
