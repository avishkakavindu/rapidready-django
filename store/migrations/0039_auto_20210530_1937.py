# Generated by Django 3.1.7 on 2021-05-30 14:07

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_auto_20210530_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='cart',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 19, 37, 34, 54493)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 19, 37, 34, 52536)),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 30, 19, 37, 34, 54493)),
        ),
    ]