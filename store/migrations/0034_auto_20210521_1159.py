# Generated by Django 3.1.7 on 2021-05-21 06:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_auto_20210519_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 21, 11, 59, 43, 8328)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 21, 11, 59, 43, 6324)),
        ),
        migrations.AlterField(
            model_name='orderedservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_set', to='store.service'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 21, 11, 59, 43, 8328)),
        ),
    ]