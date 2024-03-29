# Generated by Django 3.1.7 on 2021-05-11 07:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20210510_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='order_desc',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 13, 29, 12, 457878)),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='added_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 13, 29, 12, 457878)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 13, 29, 12, 455891)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 13, 29, 12, 456881)),
        ),
    ]
