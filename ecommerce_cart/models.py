from django.db import models
from django_extensions.db.models import TimeStampedModel

from ecommerce_products.models import Product
from ecommerce_users.models import CustomUser
from utils.model_abstracts import Model


class ShoppingSession(Model, TimeStampedModel):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name='shopping_session',
                                verbose_name='user_id')
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)


class CartProduct(Model, TimeStampedModel):
    shopping_session = models.ForeignKey(to=ShoppingSession, on_delete=models.CASCADE, related_name='cart_product',
                                         verbose_name='shopping_session_id')
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE, related_name='cart_product',
                                   verbose_name='product_id')
    quantity = models.PositiveIntegerField(null=False, default=1)
