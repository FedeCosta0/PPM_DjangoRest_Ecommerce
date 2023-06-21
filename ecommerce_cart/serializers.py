from rest_framework import serializers

from .models import ShoppingSession, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartProduct
        fields = [
            'product_id',
            'product_name',
            'price',
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
