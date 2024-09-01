# products/services.py

from decimal import Decimal
from django.db.models import Sum, F
from .models import Product, Category, Reservation
from .exceptions import ProductNotFoundError, InsufficientStockError, ReservationError


# products/services.py

from decimal import Decimal
from django.db.models import Sum, F
from .models import Product, Category, Reservation
from .exceptions import ProductNotFoundError, InsufficientStockError, ReservationError


class ProductService:

    @staticmethod
    def list_products(category_id=None):
        queryset = Product.objects.filter(stock__gt=0)
        if category_id:
            category = Category.objects.get(pk=category_id)
            subcategories = category.subcategories.all()
            queryset = queryset.filter(category__in=[category] + list(subcategories))
        return queryset

    @staticmethod
    def get_product(pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise ProductNotFoundError(f"Product with id {pk} not found.")

    @staticmethod
    def modify_stock(product, quantity):
        """
        Modify the stock of a product. Positive quantity increases stock, negative quantity decreases stock.
        """
        if product.stock + quantity < 0:
            raise InsufficientStockError("Not enough stock available.")
        product.stock += quantity
        product.save()

    @staticmethod
    def start_sale(pk, discount):
        product = ProductService.get_product(pk)
        product.discount = Decimal(discount)
        product.save()
        return product

    @staticmethod
    def end_sale(pk):
        product = ProductService.get_product(pk)
        product.discount = Decimal(0)
        product.save()
        return product

    @staticmethod
    def get_sold_products_report(start_date=None, end_date=None, category=None):
        queryset = Product.objects.filter(reservation__status="sold")
        queryset = queryset.annotate(
            total_sold=Sum("reservation__quantity"),
            total_revenue=Sum(F("reservation__quantity") * F("price")),
        ).filter(total_sold__gt=0)

        if start_date and end_date:
            queryset = queryset.filter(
                reservation__updated_at__range=[start_date, end_date]
            )
        if category:
            queryset = queryset.filter(category=category)

        return queryset


class CategoryService:

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category(category_id):
        return Category.objects.get(pk=category_id)


class ReservationService:

    @staticmethod
    def get_all_reservations():
        return Reservation.objects.all()

    @staticmethod
    def create_reservation(data):
        product = ProductService.get_product(data.get("product"))
        quantity = int(data.get("quantity", 1))
        user = data.get("user", "Anonymous")
        ProductService.modify_stock(product, -quantity)  # Decrease stock
        reservation = Reservation.objects.create(
            product=product, quantity=quantity, user=user
        )
        return reservation

    @staticmethod
    def complete_sale(reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        if reservation.status != "reserved":
            raise ReservationError("Reservation is not available for sale.")
        reservation.status = "sold"
        reservation.save()
        return reservation

    @staticmethod
    def cancel_reservation(reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        if reservation.status == "sold":
            raise ReservationError("Reservation already completed. Cannot cancel.")
        product = reservation.product
        ProductService.modify_stock(product, reservation.quantity)  # Increase stock
        reservation.status = "canceled"
        reservation.save()
        return reservation
