from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from order.models import Vendor, SKU, Item, Order, Chip
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
            weight = weight + item.sku.weight*item.quantity
        return Response({'weight': weight})


def make_order(request, chip):
    chip = Chip.objects.all().filter(tag=chip)
    if chip.exists():
        order = Order(
            chip=chip[0]
        )
        order.save()

        return HttpResponse('{ "order" : ' + str(order.id) + '}')
    else:
        return HttpResponse('{-1}')

# TODO: Android api: change item: order_id, item_id, qty, if qty 0, remove

def add_item(request, chip_id, rf_id):
    order = Order.objects.all().filter(chip__tag=chip_id).order_by('-created')
    if len(order) > 0:
        order = order[0]
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
        order = Order.objects.all().filter(chip=chip_id).order_by('-created')
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
