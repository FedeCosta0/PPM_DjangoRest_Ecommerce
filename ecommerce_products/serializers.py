from collections import OrderedDict

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework import serializers

from .models import Product, ProductCategory, ProductInventory, Discount


class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'There is not enough stock'
    default_code = 'invalid'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
        ]

    def create(self, validated_data):
        product_inventory = validated_data.pop('initial_quantity')
        product_inventory_instance = ProductInventory.objects.create(quantity=product_inventory)
        product_instance = Product.objects.create(**validated_data, inventory=product_inventory_instance)
        return product_instance


class ProductCategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Product.objects.all())

    class Meta:
        model = ProductCategory
        fields = [
            'name',
            'description',
            'products',
        ]


class ProductInventorySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Product.objects.all())

    class Meta:
        model = ProductInventory
        fields = [
            'quantity',
            'product',
        ]


class DiscountSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Product.objects.all())

    class Meta:
        model = Discount
        fields = [
            'name',
            'description',
            'discount_percent',
            'active',
            'products',
        ]


"""
class OrderSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=False)

    class Meta:
        model = Order
        fields = (
            'item',
            'quantity',
        )

    def validate(self, res: OrderedDict):
        
        item = res.get("item")
        quantity = res.get("quantity")
        if not item.check_stock(quantity):
            raise NotEnoughStockException
        return res

"""
