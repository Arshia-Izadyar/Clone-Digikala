# Generated by Django 4.2 on 2023-07-14 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraddress",
            name="city",
            field=models.CharField(
                default="Tehran", max_length=40, verbose_name="City"
            ),
        ),
        migrations.AddField(
            model_name="useraddress",
            name="state",
            field=models.CharField(
                default="Tehran", max_length=40, verbose_name="State"
            ),
        ),
    ]
