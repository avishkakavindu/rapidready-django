# Generated by Django 3.1.7 on 2021-05-30 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_auto_20210530_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 18, 27, 20, 431224)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 18, 27, 20, 429225)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 18, 27, 20, 431224)),
        ),
    ]
