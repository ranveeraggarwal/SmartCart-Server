import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from order.models import Vendor, SKU, Item, Order, Chip, OrderStatusOptions
from order.serializers import VendorSerializer, SKUSerializer, ItemSerializer, OrderSerializer, ChangeItemSerializer


class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()


class SKUViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SKUSerializer
    queryset = SKU.objects.all()


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    @detail_route(methods=['POST'])
    def update_item(self, request, pk):
        serialized_data = ChangeItemSerializer(data=request.data)
        item = self.get_object()
        if serialized_data.is_valid():
            if serialized_data.validated_data['quantity'] == 0:
                item.delete()
                return Response({'delete': 'success'})
            else:
                try:
                    item.quantity = serialized_data.validated_data['quantity']
                except KeyError:
                    pass
                item.save()
                return Response(ItemSerializer(item).data)
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @detail_route()
    def get_weight(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        items = order.item_order.all()
        weight = 0
        for item in items:
            weight = weight + item.sku.weight * item.quantity
        return Response({'weight': weight})

    @detail_route()
    def set_completed(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = OrderStatusOptions.COMPLETED
        order.save()

        return Response({'success': True})

    @detail_route()
    def set_cancelled(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = OrderStatusOptions.CANCELLED
        order.save()

        return Response({'success': True})


def make_order(request, chip_id):
    chip = Chip.objects.all().filter(tag=chip_id)
    if chip.exists():
        old_order = Order.objects.all().filter(chip__tag=chip_id, status=OrderStatusOptions.PENDING).order_by(
            '-created')
        new_order = Order(
                chip=chip[0]
        )

        save_new = True
        if len(old_order) >= 0:
            order = old_order[0]
            order_id = order.id

            now_ts = datetime.datetime.now().timestamp()
            create_ts = order.created.timestamp()
            t = now_ts - create_ts
            if t < 5 * 60:
                save_new = False
                order.created = datetime.datetime.now()
                order.save()

        if save_new:
            new_order.save()
            order_id = new_order.id

        return HttpResponse('{ "order" : ' + str(order_id) + '}')
    else:
        return HttpResponse('{ "order" : -1 }')


# TODO: Android api: change item: order_id, item_id, qty, if qty 0, remove

def add_item(request, chip_id, rf_id):
    order = Order.objects.all().filter(chip__tag=chip_id).order_by('-created')
    if len(order) > 0:
        order = order[0]
        order.created = datetime.datetime.now()
        order.save()
        sku = SKU.objects.all().filter(rfid=rf_id)
        if len(sku) == 0:
            return HttpResponse('{-1}')
        sku = sku[0]
        item = Item.objects.all().filter(order=order, sku=sku)
        if len(item) > 0:
            item = item[0]
            item.quantity += 1
            item.save()
        else:
            item = Item(
                    sku=sku,
                    quantity=1,
                    order=order,
            )
            item.save()
        return HttpResponse('{' + str(sku.title) + ' Rs.' + str(sku.price) + '/-}')
    else:
        return HttpResponse('{-1}')


def verify_weight(request, chip_id, cart_weight):
    order = Order.objects.all().filter(chip__tag=chip_id).order_by('-created')
    if len(order) == 0:
        return HttpResponse('{-1}')
    order = order[0]
    order.cart_weight = cart_weight
    order.created = datetime.datetime.now()
    order.save()

    items = order.item_order.all()
    weight = 0
    for item in items:
        weight = weight + item.sku.weight * item.quantity

    top_limit = cart_weight * 115 / 100
    bot_limit = cart_weight * 85 / 100

    if bot_limit < weight < top_limit:
        return HttpResponse('{1}')
    else:
        return HttpResponse('{0}')
