from django.db import models


class SKU(models.Model):
    title = models.CharField(max_length=64)
    weight = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)


class Order(models.Model):
    username = models.CharField(max_length=64)


class Item(models.Model):
    sku = models.ForeignKey(SKU, related_name='item_sku')
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='item_order')


