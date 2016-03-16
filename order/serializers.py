from rest_framework import serializers

from .models import Vendor, SKU, Order, Item


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor


class SKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
