from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    ReservationSerializer,
    SoldProductReportSerializer,
)
from .services import ProductService, CategoryService, ReservationService


class ProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of products, optionally filtered by category.",
        responses={200: ProductSerializer(many=True)},
        query_parameters=[
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get_queryset(self):
        category_id = self.request.query_params.get("category", None)
        return ProductService.list_products(category_id=category_id)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = ProductService.list_products()

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a product by ID.",
        responses={200: ProductSerializer()},
    )
    def get_object(self):
        product_id = self.kwargs.get("pk")
        return ProductService.get_product(product_id)


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of categories.",
        responses={200: CategorySerializer(many=True)},
    )
    def get_queryset(self):
        return CategoryService.get_all_categories()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryService.get_all_categories()

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a category by ID.",
        responses={200: CategorySerializer()},
    )
    def get_object(self):
        category_id = self.kwargs.get("pk")
        return CategoryService.get_category(category_id)


class ReservationListView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a list of reservations.",
        responses={200: ReservationSerializer(many=True)},
    )
    def get_queryset(self):
        return ReservationService.get_all_reservations()

    @swagger_auto_schema(
        operation_description="Create a new reservation.",
        request_body=ReservationSerializer,
        responses={201: ReservationSerializer()},
    )
    def create(self, request, *args, **kwargs):
        reservation = ReservationService.create_reservation(request.data)
        return Response(
            ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED
        )


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    queryset = ReservationService.get_all_reservations()

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a reservation by ID.",
        responses={200: ReservationSerializer()},
    )
    def get_object(self):
        reservation_id = self.kwargs.get("pk")
        return ReservationService.get_reservation(reservation_id)


class ReservationCancelView(generics.UpdateAPIView):
    serializer_class = ReservationSerializer
    queryset = ReservationService.get_all_reservations()

    @swagger_auto_schema(
        operation_description="Cancel a reservation by ID.",
        responses={200: ReservationSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        reservation_id = self.kwargs.get("pk")
        reservation = ReservationService.cancel_reservation(reservation_id)
        return Response(ReservationSerializer(reservation).data)


class CompleteSaleView(generics.UpdateAPIView):
    serializer_class = ReservationSerializer
    queryset = ReservationService.get_all_reservations()

    @swagger_auto_schema(
        operation_description="Mark a reservation as sold.",
        responses={200: ReservationSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        reservation_id = self.kwargs.get("pk")
        reservation = ReservationService.complete_sale(reservation_id)
        return Response(ReservationSerializer(reservation).data)


class StartSaleView(APIView):
    queryset = ProductService.list_products()

    @swagger_auto_schema(
        operation_description="Start a sale on a product by providing a discount percentage.",
        responses={200: "Sale started successfully."},
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="Product ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "discount",
                openapi.IN_PATH,
                description="Discount percentage",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def post(self, request, pk, discount):
        product = ProductService.start_sale(pk, discount)
        return Response(
            {
                "status": "sale started",
                "original_price": product.price,
                "discounted_price": product.get_discounted_price(),
                "discount": product.discount,
            },
            status=status.HTTP_200_OK,
        )


class EndSaleView(APIView):
    @swagger_auto_schema(
        operation_description="End the sale on a product.",
        responses={200: "Sale ended successfully."},
        manual_parameters=[
            openapi.Parameter(
                "pk",
                openapi.IN_PATH,
                description="Product ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def post(self, request, pk):
        product = ProductService.end_sale(pk)
        return Response(
            {
                "status": "sale ended",
                "original_price": product.price,
                "current_price": product.get_discounted_price(),
            },
            status=status.HTTP_200_OK,
        )


class SoldProductReportView(generics.ListAPIView):
    serializer_class = SoldProductReportSerializer

    @swagger_auto_schema(
        operation_description="Get a report of sold products, optionally filtered by date range and category.",
        responses={200: SoldProductReportSerializer(many=True)},
        query_parameters=[
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                description="Filter by start date",
                type=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                description="Filter by end date",
                type=openapi.FORMAT_DATE,
            ),
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get_queryset(self):
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        category = self.request.query_params.get("category")
        return ProductService.get_sold_products_report(start_date, end_date, category)
