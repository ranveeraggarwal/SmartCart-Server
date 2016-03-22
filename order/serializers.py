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
    sku = SKUSerializer(read_only=True)
    class Meta:
        model = Item


class WeightSerializer(serializers.Serializer):
    weight = serializers.FloatField(default=0.0)
