# Generated by Django 4.0.5 on 2022-08-30 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_user_more_detail_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='sold_stock_unit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_stock_unit',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
