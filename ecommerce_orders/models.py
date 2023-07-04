from django.db import models
from django_extensions.db.models import TimeStampedModel

from ecommerce_products.models import Product
from ecommerce_users.models import CustomUser
from utils.model_abstracts import Model


class Order(Model, TimeStampedModel):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)


class PaymentDetails(Model, TimeStampedModel):
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, related_name='payment_details')
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    provider = models.CharField(max_length=50, null=False)
    status = models.PositiveIntegerField(null=False, default=0)


class OrderProduct(Model, TimeStampedModel):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.PositiveIntegerField(null=False, default=1)
