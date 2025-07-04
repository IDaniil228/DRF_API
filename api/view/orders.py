from django.db.models import Max

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import ProductFilter
from api.models import Product, Order
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("products")
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)