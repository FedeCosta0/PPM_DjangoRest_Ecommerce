from rest_framework import serializers

from ecommerce_orders.models import Order, OrderProduct, PaymentDetails


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        models = OrderProduct
        fields = ['product', 'quantity', ]


class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = ['amount', 'provider', 'status', ]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)
    payment_details = PaymentDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'total', 'products', 'payment_details', ]
