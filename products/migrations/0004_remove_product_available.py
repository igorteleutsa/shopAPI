# Generated by Django 5.1 on 2024-09-01 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_rename_reserved_at_reservation_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="available",
        ),
    ]
