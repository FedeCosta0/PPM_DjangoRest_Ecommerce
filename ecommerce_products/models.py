from django.db import models
from django.db.models.signals import pre_save, post_save
from django_extensions.db.models import (
    TimeStampedModel
)

from utils.model_abstracts import Model
from utils.slugify import slugify_instance_name


class ProductCategory(Model, TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ["name"]


class ProductInventory(Model, TimeStampedModel):
    stock = models.PositiveIntegerField(null=False, default=1)

    def add_stock(self, qty):
        new_stock = self.stock + int(qty)
        self.stock = new_stock
        self.save()

    def reduce_stock(self, qty):
        new_stock = self.stock - int(qty)
        self.stock = new_stock
        self.save()

    def check_stock(self, qty):
        if int(qty) > self.stock:
            return False
        return True


class Discount(Model, TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0.00)
    active = models.BooleanField(null=False, default=False)


class Product(Model, TimeStampedModel):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.DO_NOTHING, related_name='products')
    inventory = models.OneToOneField(to=ProductInventory, on_delete=models.DO_NOTHING, related_name='product')
    discount = models.ForeignKey(to=Discount, on_delete=models.DO_NOTHING, related_name='products')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ["name"]

    def __str__(self):
        return self.name


def product_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_name(instance, save=False)


pre_save.connect(product_pre_save, sender=Product)


def product_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created:
        slugify_instance_name(instance, save=True)


post_save.connect(product_post_save, sender=Product)


def category_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_name(instance, save=False)


pre_save.connect(category_pre_save, sender=ProductCategory)


def category_post_save(sender, instance, created, *args, **kwargs):
    # print('post_save')
    if created:
        slugify_instance_name(instance, save=True)


post_save.connect(category_post_save, sender=ProductCategory)
