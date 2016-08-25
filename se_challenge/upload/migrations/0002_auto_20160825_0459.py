# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='pre_tax_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expense',
            name='tax_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
