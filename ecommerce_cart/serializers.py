from rest_framework import serializers

from .models import ShoppingSession, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    name = serializers.ReadOnlyField(source='product.name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartProduct
        fields = [
            'product_id',
            'id',
            'name',
            'price',
            'quantity'
        ]


class CartProductCreationSerializer(serializers.ModelSerializer):
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
