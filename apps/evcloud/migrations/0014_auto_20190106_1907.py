# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-06 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evcloud', '0013_auto_20190106_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiauth',
            name='description',
            field=models.CharField(default='', max_length=50, verbose_name='描述'),
        ),
    ]
