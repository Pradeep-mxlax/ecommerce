# Generated by Django 4.0.5 on 2022-09-02 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_alter_offer_category_alter_offer_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='discount_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
