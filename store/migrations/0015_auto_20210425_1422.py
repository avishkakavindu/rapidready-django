# Generated by Django 3.1.7 on 2021-04-25 08:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20210425_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 25, 14, 22, 36, 607625)),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 25, 14, 22, 36, 609618)),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='added_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 25, 14, 22, 36, 609618)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 25, 14, 22, 36, 609618)),
        ),
    ]
