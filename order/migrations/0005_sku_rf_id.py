# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-22 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_order_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='rf_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
