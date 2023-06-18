# Register your models here.
from django.contrib import admin

from . import models


@admin.register(models.ShoppingSession)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total')


@admin.register(models.CartProduct)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopping_session', 'product', 'quantity')
