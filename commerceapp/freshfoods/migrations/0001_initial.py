# Generated by Django 3.2.25 on 2024-05-12 03:55

import compressed_image_field
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streetname', models.CharField(max_length=100, null=True)),
                ('streetnumber', models.IntegerField(null=True)),
                ('postcode', models.CharField(max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='cart_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='payment_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(null=True)),
                ('exp_number', models.DateField(null=True)),
                ('cvc_number', models.IntegerField(null=True)),
                ('cardholder', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='shoppingcart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(default=None, to='freshfoods.cart_item')),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='profileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', compressed_image_field.CompressedImageField(default='default_profile.jpg', null=True, quality=10, upload_to='profiles')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='freshfoods.adress')),
                ('payment_info', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='freshfoods.payment_info')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('discription', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=18, null=True)),
                ('discount', models.IntegerField(default=0, null=True)),
                ('img', compressed_image_field.CompressedImageField(default='default_product.jpg', null=True, quality=50, upload_to='products')),
                ('lastupdate', models.DateTimeField(auto_now_add=True, null=True)),
                ('tags', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='freshfoods.tag')),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.CharField(auto_created=True, blank=True, max_length=50, null=True, unique=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PACKING', 'PACKING'), ('ON THE WAY', 'ON THE WAY'), ('COMPLETED', 'COMPLETED'), ('REJECTED', 'REJECTED')], default=1, max_length=50)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('product', models.ManyToManyField(to='freshfoods.cart_item')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cart_item',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='freshfoods.product'),
        ),
        migrations.AddField(
            model_name='cart_item',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
