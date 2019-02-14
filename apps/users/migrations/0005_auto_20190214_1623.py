# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-14 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_authkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authkey',
            name='permission',
            field=models.IntegerField(choices=[(0, '可读可写'), (1, '只读')], default=0, verbose_name='读写权限'),
        ),
    ]
