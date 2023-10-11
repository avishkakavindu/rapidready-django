# Generated by Django 3.1.7 on 2021-04-04 05:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_material_servicematerial_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='material',
            name='unit_price',
        ),
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='service',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='quantity',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='rating',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='stock',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='servicematerial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.material'),
        ),
        migrations.AlterField(
            model_name='servicematerial',
            name='quantity',
            field=models.DecimalField(decimal_places=2, help_text='Material needed for one unit. Ex: 1 business card 1/20 of 14pt business card stock paper', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='stock',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.material'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(blank=True, null=True)),
                ('rating', models.DecimalField(decimal_places=0, default=0, max_digits=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.service')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.service')),
            ],
        ),
    ]
