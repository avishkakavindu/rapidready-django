# Generated by Django 3.1.7 on 2021-03-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210312_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Customer'), (2, 'Supplier'), (3, 'Production Manager'), (4, 'Production Team'), (5, 'Store Manager'), (6, 'Store Team')], null=True),
        ),
    ]