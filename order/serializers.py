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

    @staticmethod
    def get_items(order: Order):
        items_order = order.item_order.all()
        return ItemSerializer(items_order, many=True).data

    class Meta:
        model = Order
        fields = ['id', 'shop', 'cart_weight', 'items', 'created']


class ItemSerializer(serializers.ModelSerializer):
    sku = SKUSerializer(read_only=True)

    class Meta:
        model = Item


class WeightSerializer(serializers.Serializer):
    weight = serializers.FloatField(default=0.0)


class ChangeItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()