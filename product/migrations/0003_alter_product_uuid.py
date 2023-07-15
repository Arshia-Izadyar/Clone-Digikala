# Generated by Django 4.2 on 2023-07-15 11:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_alter_product_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="uuid",
            field=models.CharField(default=uuid.uuid4, max_length=150, unique=True),
        ),
    ]
