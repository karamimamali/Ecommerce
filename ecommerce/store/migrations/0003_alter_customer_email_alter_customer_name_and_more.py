# Generated by Django 4.2.4 on 2023-09-15 08:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="customer",
            name="name",
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
