from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from yaml import serialize

from api.filters import OrderFilter
from api.models import Order
from api.serializers import OrderSerializer
from api.serializers.orders import OrderCreateSerializer


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("products")
#     serializer_class = OrderSerializer
#
#
# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("products")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    @method_decorator(cache_page(60, key_prefix="orders-list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PUT":
            return OrderCreateSerializer
        return super().get_serializer_class()


    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_anonymous:
            if not self.request.user.is_staff:
                qs = qs.filter(user=self.request.user)
        return qs

    # @action(detail=False,
    #         methods=["get"],
    #         permission_classes=[IsAuthenticated],
    #         url_path="user-orders")
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)

