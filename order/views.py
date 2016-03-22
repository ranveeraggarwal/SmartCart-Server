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


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
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

    @detail_route()
    def get_items(self, request, pk):
        """
        Get items of an order id
        ---
        response_serializer: ItemSerializer
        """
        order = get_object_or_404(Order, pk=pk)
        order_items = order.item_order.all()
        items = ItemSerializer(order_items, many=True, context={'request': request})
        return Response({'items': items.data})


def make_order(request, vendor_id):
    vendor = Vendor.objects.all().filter(id=vendor_id)
    if vendor.exists():
        order = Order(
            shop=vendor[0]
        )
        order.save()
        return HttpResponse('{'+str(order.id)+'}')
    else:
        return HttpResponse('{-1}')

# TODO: Android api: change item: order_id, item_id, qty, if qty 0, remove


def add_item(request, order_id, rf_id):
    order = Order.objects.all().filter(id=order_id)
    if len(order) > 0:
        order = order[0]
        sku = SKU.objects.all().filter(rf_id=rf_id)
        if len(sku) == 0:
            return HttpResponse('{-1}')
        sku = sku[0]
        item = Item.objects.all().filter(order=order, sku=sku)
        if len(item) > 0:
            item[0].quantity += 1
            item[0].save()
            return HttpResponse('{' + str(order_id) + ' ' + str(item[0].id) + ' ' + str(item[0].quantity) + '}')
        else:
            item = Item(
                sku=sku,
                quantity=1,
                order=order,
            )
            item.save()
            return HttpResponse('{' + str(order_id) + ' ' + str(item.id) + ' ' + str(item.quantity) + '}')
    else:
        return HttpResponse('{-1}')


def verify_weight(request, order_id, cart_weight):
        order = Order.objects.all().filter(id=order_id)
        if len(order) == 0:
            return HttpResponse('{-1}')
        order = order[0]
        order.cart_weight = cart_weight
        order.save()
        items = order.item_order.all()
        weight = 0
        for item in items:
            weight = weight + item.sku.weight*item.quantity
        print(weight)
        if int(cart_weight) == int(weight):
            return HttpResponse('{1}')
        else:
            return HttpResponse('{0}')
