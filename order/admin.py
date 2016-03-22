from django.contrib import admin

from .models import Vendor, SKU, Order, Item


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'weight', 'price', 'rf_id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'cart_weight']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'quantity', 'order']
