# Generated by Django 4.2 on 2023-07-14 12:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_useraddress_city_useraddress_state"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="user_score",
            new_name="score",
        ),
    ]