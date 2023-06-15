from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import (
    TimeStampedModel
)

from utils.model_abstracts import Model


class ProductCategory(Model, TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)


class ProductInventory(Model, TimeStampedModel):
    stock = models.PositiveIntegerField(null=False, default=1)

    def manage_stock(self, qty):
        # used to reduce Product stock
        new_stock = self.stock - int(qty)
        self.stock = new_stock
        self.save()

    def check_stock(self, qty):
        # used to check if order quantity exceeds stock levels
        if int(qty) > self.stock:
            return False
        return True

    '''
    def place_order(self, user, qty):
        # used to place an order
        if self.check_stock(qty):
            order = Order.objects.create(
                item=self,
                quantity=qty,
                user=user)
            self.manage_stock(qty)
            return order
        else:
        
    '''


class Discount(Model, TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0.00)
    active = models.BooleanField(null=False, default=False)


class Product(Model, TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.DO_NOTHING, related_name='products', verbose_name='category_id')
    inventory = models.OneToOneField(to=ProductInventory, on_delete=models.DO_NOTHING, related_name='product', verbose_name='inventory_id')
    discount = models.ForeignKey(to=Discount, on_delete=models.DO_NOTHING, related_name='products', verbose_name='discount_id')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ["id"]

    def __str__(self):
        return self.name


