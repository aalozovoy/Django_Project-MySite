# Generated by Django 5.0.1 on 2024-02-19 17:36

import shopapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0008_order_receipt_alter_product_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to=shopapp.models.product_preview_dir_path),
        ),
    ]
