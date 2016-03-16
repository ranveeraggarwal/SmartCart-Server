from django.db import models


class SKU(models.Model):
    title = models.CharField(max_length=64)
    weight = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)


class Item(models.Model):
    sku = models.ForeignKey(SKU, related_name='item_sku')
    quantity = models.IntegerField()


class Order(models.Model):
    items = models.ManyToManyField(Item, related_name='order_item', blank=True)
