from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from order.models import Vendor, SKU, Item, Order
from order.serializers import VendorSerializer, SKUSerializer, ItemSerializer, OrderSerializer, WeightSerializer


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()


class SKUViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SKUSerializer
    queryset = SKU.objects.all()


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @detail_route()
    def get_weight(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        items = order.item_order.all()
        weight = 0
        for item in items:
            weight = weight + item.sku.weight*item.quantity
        return Response({'weight': weight})

