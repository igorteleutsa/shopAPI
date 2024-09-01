from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, Category, Reservation


class ProductTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest model",
            price="999.99",
            stock=10,
            category=self.category,
        )
        self.reservation = Reservation.objects.create(
            product=self.product, user="testuser", status="reserved", quantity=1
        )

    def test_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Smartphone")

    def test_product_detail(self):
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Smartphone")

    def test_product_create(self):
        url = reverse("product-list")
        data = {
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": "1299.99",
            "stock": 5,
            "category": self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_nonexistent_product(self):
        response = self.client.get("/api/products/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_reservation_insufficient_stock(self):
        data = {"product": self.product.id, "quantity": 20}
        response = self.client.post("/api/reservations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Not enough stock available", response.data["detail"])

    def test_reservation_create(self):
        url = reverse("reservation_list")
        data = {"product": self.product.id, "user": "testuser2", "quantity": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)  # Stock should decrease

    def test_reservation_cancel(self):
        url = reverse("reservation-cancel", args=[self.reservation.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "canceled")
        self.reservation.product.refresh_from_db()
        self.assertEqual(self.reservation.product.stock, 11)  # Stock should be restored

    def test_start_sale(self):
        url = reverse("start_sale", args=[self.product.id, 20])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.discount, 20)

    def test_sold_product_report(self):
        self.reservation.status = "sold"
        self.reservation.save()
        url = reverse("sold_report")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["total_sold"], 1)
