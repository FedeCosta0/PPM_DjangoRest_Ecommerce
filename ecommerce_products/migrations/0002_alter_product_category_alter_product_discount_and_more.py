# Generated by Django 4.1.9 on 2023-06-22 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='ecommerce_products.productcategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='ecommerce_products.discount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='inventory',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='product', to='ecommerce_products.productinventory'),
        ),
    ]
