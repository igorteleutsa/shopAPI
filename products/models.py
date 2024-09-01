from decimal import Decimal

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0))

    def get_discounted_price(self):
        return self.price * (Decimal(1) - self.discount / Decimal(100))

    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(
        max_length=100
    )  # This should be a ForeignKey to User in a real application
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="reserved")
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} reserved by {self.user}"
