# Generated by Django 3.1.7 on 2021-05-13 09:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_auto_20210513_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 14, 37, 17, 213051)),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cartservice_set', to='store.service'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 14, 37, 17, 211048)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 14, 37, 17, 213051)),
        ),
    ]
