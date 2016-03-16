from rest_framework import viewsets
from order.models import Vendor, SKU, Item, Order
from order.serializers import VendorSerializer, SKUSerializer, ItemSerializer, OrderSerializer


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
