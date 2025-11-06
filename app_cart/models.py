from django.db import models
from django.conf import settings
from app_products.models import Product
import uuid


class Cart(models.Model):
    """Modelo para el carrito de compras"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        ordering = ['-updated_at']

    def __str__(self):
        if self.user:
            return f"Carrito de {self.user.username}"
        return f"Carrito (Sesión: {self.session_key})"

    def get_total(self):
        """Calcula el total del carrito"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_total_items(self):
        """Obtiene el número total de artículos en el carrito"""
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        """Limpia todos los items del carrito"""
        self.items.all().delete()


class CartItem(models.Model):
    """Modelo para los items del carrito"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ('cart', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    def get_subtotal(self):
        """Calcula el subtotal del item"""
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        """Valida el stock antes de guardar"""
        if self.quantity > self.product.stock:
            raise ValueError(f"No hay suficiente stock. Stock disponible: {self.product.stock}")
        super().save(*args, **kwargs)
