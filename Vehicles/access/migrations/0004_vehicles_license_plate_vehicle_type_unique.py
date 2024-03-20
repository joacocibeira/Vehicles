# Generated by Django 4.2.11 on 2024-03-20 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("access", "0003_remove_vehicles_unique_vehicle_remove_vehicles_id_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="vehicles",
            constraint=models.UniqueConstraint(
                fields=("license_plate", "vehicle_type"),
                name="license_plate_vehicle_type_unique",
            ),
        ),
    ]