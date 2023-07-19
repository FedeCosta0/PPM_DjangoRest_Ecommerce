from django.contrib import admin

from . import models


@admin.register(models.ShoppingSession)
class ShoppingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total')


@admin.register(models.CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopping_session', 'product', 'quantity')
