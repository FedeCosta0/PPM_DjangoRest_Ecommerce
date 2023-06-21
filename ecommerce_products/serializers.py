from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

from .models import Product, ProductCategory, ProductInventory, Discount


class NotEnoughStockException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'There is not enough stock'
    default_code = 'invalid'


class ProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
        ]

    def create(self, validated_data):
        inventory_instance = ProductInventory.objects.create()
        discount_instance, created = Discount.objects.get_or_create(name="NullDiscount")
        product_instance = Product.objects.create(**validated_data, inventory=inventory_instance,
                                                  discount=discount_instance)
        return product_instance


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    discount = serializers.ReadOnlyField(source='discount.discount_percent')
    is_discount_active = serializers.ReadOnlyField(source='discount.active')

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
            'discount',
            'is_discount_active',
        ]


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
            'stock',
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
