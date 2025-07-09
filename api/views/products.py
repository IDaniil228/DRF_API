from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import ProductFilter
from api.models import Product
from api.serializers import ProductSerializer, ProductInfoSerializer



class ProductsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()

    search_fields = ["name", "description"]
    ordering_fields = ["price"]

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
           self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductsDetailListAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()



class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)