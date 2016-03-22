from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class SKU(models.Model):
    title = models.CharField(max_length=64)
    weight = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)
    rf_id = models.IntegerField()
    picture = models.ImageField(blank=None, null=None, default='')

    def __str__(self):
        return self.title


class Order(models.Model):
    shop = models.ForeignKey(Vendor, related_name='order_vendor')
    created = models.DateTimeField(auto_now_add=True)
    cart_weight = models.FloatField(default=0.0)


class Item(models.Model):
    sku = models.ForeignKey(SKU, related_name='item_sku')
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='item_order')
