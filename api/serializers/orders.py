from rest_framework import serializers

from django.db import transaction

from api.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    # products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializers(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ["product", "quantity"]

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializers(many=True)

    def create(self, validated_data):
        order_items = validated_data.pop("items")
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item in order_items:
                OrderItem.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        items = validated_data.pop("items")
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if items is not None:
                instance.items.all().delete()

            for item in items:
                OrderItem.objects.create(order=instance, **item)
        return instance

    class Meta:
        model = Order
        fields = ["order_id", "user", "status", "items"]
        extra_kwargs = {
            "user" : {"read_only" : True}
        }