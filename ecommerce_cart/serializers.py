from rest_framework import serializers

from .models import ShoppingSession, CartProduct


class ShoppingSessionSerializer(serializers.ModelSerializer):
    cart_product = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = ShoppingSession
        fields = [
            'user',
            'total',
            'cart_product'
        ]


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [
            'shopping_session',
            'product',
            'quantity'
        ]
