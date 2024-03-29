# Generated by Django 3.1.7 on 2021-03-14 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20210313_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_unit', models.PositiveIntegerField()),
                ('warning_limit', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.CharField(max_length=255)),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.material')),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.material')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.service')),
            ],
        ),
    ]
