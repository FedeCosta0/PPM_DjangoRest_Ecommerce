from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'category', 'inventory', 'discount')


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(models.ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock')


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'discount', 'active')
