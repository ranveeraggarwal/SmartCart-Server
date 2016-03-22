from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
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

    @detail_route(methods=['POST'])
    def verify_weight(self, request, pk):
        """
        Verify Weight
        ---
        request_serializer: WeightSerializer
        """
        order = self.get_object()
        serialized_data = WeightSerializer(data=request.data)
        if serialized_data.is_valid():
            order.cart_weight = serialized_data.validated_data['weight']
        items = order.item_order.all()
        weight = 0
        for item in items:
            weight = weight + item.sku.weight*item.quantity
        if order.cart_weight == weight:
            return Response({'equal': True})
        else:
            return Response({'equal': False})


def make_order(request, vendor_id):
    vendor = Vendor.objects.all().filter(id=vendor_id)
    if vendor.exists():
        order = Order(
            shop=vendor[0]
        )
        order.save()
        return HttpResponse(order.id)
    else:
        return HttpResponse(-1)
