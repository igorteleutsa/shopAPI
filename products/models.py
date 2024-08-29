from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    product = models.ForeignKey(Product, related_name='reservations', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    reserved_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
