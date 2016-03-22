from rest_framework import serializers

from .models import Vendor, SKU, Order, Item


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor


class SKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, order: Order):
        items = order.item_order.all()
        serialized_items = []
        for item in items:
            serialized_items.append(ItemSerializer(item))
        return {'items': serialized_items}

    class Meta:
        model = Order
        fields = ['id', 'shop', 'cart_weight', 'items', 'created']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item


class WeightSerializer(serializers.Serializer):
    weight = serializers.FloatField(default=0.0)
