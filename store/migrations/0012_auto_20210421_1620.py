# Generated by Django 3.1.7 on 2021-04-21 10:50

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210421_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=datetime.datetime(2021, 4, 21, 16, 20, 32, 264196))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cart_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 21, 16, 20, 32, 264196)),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('added_on', models.DateTimeField(default=datetime.datetime(2021, 4, 21, 16, 20, 32, 265184))),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitem_set', to='store.cart')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cartservice_set', to='store.service')),
            ],
        ),
    ]