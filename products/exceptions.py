from rest_framework.exceptions import APIException


class ProductNotFoundError(APIException):
    status_code = 404
    default_detail = "Product not found."


class InsufficientStockError(APIException):
    status_code = 400
    default_detail = "Not enough stock available."


class ReservationError(APIException):
    status_code = 400
    default_detail = "Reservation error occurred."
