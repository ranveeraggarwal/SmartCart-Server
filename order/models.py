from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Chip(models.Model):
    tag = models.CharField(max_length=64, blank=None, null=None, default='')
    shop = models.ForeignKey(Vendor, related_name='chip_vendor')

    def __str__(self):
        return self.tag

class SKU(models.Model):
    title = models.CharField(max_length=64)
    weight = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    rfid = models.CharField(max_length=64, blank=True, null=True, default='')
    picture = models.ImageField(blank=True, null=True, default='')

    def __str__(self):
        return self.title

class Order(models.Model):
    chip = models.ForeignKey(Chip, related_name='order_chip', blank=True, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    cart_weight = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.pk)


class Item(models.Model):
    sku = models.ForeignKey(SKU, related_name='item_sku')
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='item_order')

    def __str__(self):
        return str(self.sku)
