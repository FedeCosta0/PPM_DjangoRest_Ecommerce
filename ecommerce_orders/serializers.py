from rest_framework import serializers

from ecommerce_orders.models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderProduct
        fields = ['product_name', 'quantity', ]


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['total', 'order_products', ]


class OrderCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'total', ]
