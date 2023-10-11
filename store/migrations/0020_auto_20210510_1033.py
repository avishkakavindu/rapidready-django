# Generated by Django 3.1.7 on 2021-05-10 05:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20210506_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 10, 33, 6, 93)),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='added_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 10, 33, 6, 93)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 10, 33, 5, 997103)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 10, 33, 5, 999096)),
        ),
    ]
