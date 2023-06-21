from rest_framework import serializers

from .models import ShoppingSession, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [
            'product',
            'quantity'
        ]


class ShoppingSessionSerializer(serializers.ModelSerializer):
    cart_products = CartProductSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = ShoppingSession
        fields = [
            'user',
            'total',
            'cart_products'
        ]
