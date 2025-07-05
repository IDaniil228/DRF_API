from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
ProductInfoAPIView, ProductsDetailListAPIView, ProductsListCreateAPIView,
OrderViewSet
)


urlpatterns = [
    path('products/', ProductsListCreateAPIView.as_view()),
    path('products/info/', ProductInfoAPIView.as_view()),
    path('products/<int:product_id>', ProductsDetailListAPIView.as_view()),
]

router = DefaultRouter()
router.register("orders", OrderViewSet)
urlpatterns += router.urls