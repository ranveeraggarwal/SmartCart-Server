from django.contrib import admin

from .models import Vendor, SKU, Order, Item, Chip


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Chip)
class ChipAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'tag']


@admin.register(SKU)
class SKUAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'weight', 'price', 'rfid', 'picture']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'chip', 'cart_weight']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'sku', 'quantity', 'order']
