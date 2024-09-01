from rest_framework import serializers
from .models import Category, Product, Reservation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "category",
            "discount",
            "discounted_price",
        ]

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class SoldProductReportSerializer(serializers.ModelSerializer):
    total_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ["name", "category", "total_sold", "total_revenue"]
