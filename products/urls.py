from django.urls import path
from . import views

urlpatterns = [
    # Product CRUD
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"
    ),
    # Category CRUD
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    # Reservation CRUD
    path("reservations/", views.ReservationListView.as_view(), name="reservation_list"),
    path(
        "reservations/<int:pk>/cancel/",
        views.ReservationCancelView.as_view(),
        name="reservation-cancel",
    ),
    path(
        "reservations/<int:pk>/",
        views.ReservationDetailView.as_view(),
        name="reservation_detail",
    ),
    # Sale
    path(
        "products/start_sale/<int:pk>/<int:discount>/",
        views.StartSaleView.as_view(),
        name="start_sale",
    ),
    # Selling product
    path(
        "reservations/<int:pk>/complete_sale/",
        views.CompleteSaleView.as_view(),
        name="complete_sale",
    ),
    # Sold report
    path(
        "products/sold_report/",
        views.SoldProductReportView.as_view(),
        name="sold_report",
    ),
]
