# Generated by Django 2.2.5 on 2019-12-12 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evcloud', '0009_apiauth_center_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiauth',
            name='pool_id',
        ),
    ]
