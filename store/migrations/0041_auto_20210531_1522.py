# Generated by Django 3.1.7 on 2021-05-31 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_auto_20210531_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='raeted_on',
        ),
        migrations.AddField(
            model_name='order',
            name='rated_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 15, 22, 23, 814730)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 15, 22, 23, 821730)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 15, 22, 23, 814730)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 15, 22, 23, 821730)),
        ),
    ]
