# Generated by Django 4.2 on 2023-07-15 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shipping", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipping",
            name="is_deliverd",
            field=models.BooleanField(default=False),
        ),
    ]