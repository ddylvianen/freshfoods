# Generated by Django 3.2.25 on 2024-05-12 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshfoods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='invoice',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]