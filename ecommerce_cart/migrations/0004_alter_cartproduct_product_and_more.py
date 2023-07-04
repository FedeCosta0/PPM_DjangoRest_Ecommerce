# Generated by Django 4.1.9 on 2023-07-04 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_products', '0003_product_slug'),
        ('ecommerce_cart', '0003_alter_cartproduct_shopping_session_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='ecommerce_products.product'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='shopping_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='ecommerce_cart.shoppingsession'),
        ),
    ]
