from rest_framework import serializers

from .models import ShoppingSession, CartProduct


class ShoppingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingSession
        fields = [
            'user',
            'total',
        ]


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = [
            'shopping_session',
            'product',
            'quantity'
        ]
