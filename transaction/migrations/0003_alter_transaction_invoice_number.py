# Generated by Django 4.2 on 2023-07-15 11:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("transaction", "0002_alter_transaction_invoice_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="invoice_number",
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
