from django.db import models
from accounts.models import CustomUser
from catalog.models import Product


PAYMENT_CHOICES = [
    ("P", "Pending"),
    ("C", "Complete"),
    ("F", "Failed"),
]


class Order(models.Model):
    place_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default="P"
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        placed = f"{self.place_at:%d/%m/%Y}" if self.place_at else "—"
        try:
            customer = str(self.customer)
        except CustomUser.DoesNotExist:
            customer = "—"
        return f"Order #{self.pk} — {placed} — {customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        try:
            product = str(self.product)
        except Product.DoesNotExist:
            product = "—"
        return f"{self.quantity} × {product}"
