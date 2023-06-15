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
            'inventory',
            'discount',
        ]

    def create(self, validated_data):
        product_inventory = validated_data.pop('inventory')
        product_inventory_instance = ProductInventory.objects.create(quantity=product_inventory)
        product_instance = Product.objects.create(**validated_data, inventory=product_inventory_instance)
        return product_instance


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = [
            'name',
            'description',
        ]


class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = [
            'quantity',
        ]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'name',
            'description',
            'discount_percent',
            'active',
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