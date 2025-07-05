from rest_framework import serializers

from api.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    # items = OrderItemSerializer(many=True, read_only=True)
    # products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'