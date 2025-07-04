from django.db.models import Max

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import ProductFilter
from api.models import Product, Order
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer


class ProductsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["price"]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
           self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("products")
    serializer_class = OrderSerializer


class ProductsDetailListAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoAPIView(APIView):
     def get(self, request):
         products = Product.objects.all()
         serializer = ProductInfoSerializer({
             'products' : products,
             'count' : len(products),
             'max_price' : products.aggregate(max_price=Max('price'))['max_price']
         })
         return Response(serializer.data)