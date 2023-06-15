from django.contrib import admin

from . import models


@admin.register(models.Product)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')


