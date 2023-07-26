from decimal import Decimal

from django.db import models
from django_extensions.db.models import TimeStampedModel

from ecommerce_products.models import Product
from ecommerce_users.models import CustomUser
from utils.model_abstracts import Model


class Cart(Model, TimeStampedModel):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='cart')
    total = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal.from_float(0.00))


class CartProduct(Model, TimeStampedModel):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='cart_products')
    quantity = models.PositiveIntegerField(null=False, default=1)

    def is_available(self):
        return self.product.inventory.check_stock(self.quantity)

    def reduce_stock_from_inventory(self):
        self.product.inventory.reduce_stock(self.quantity)
