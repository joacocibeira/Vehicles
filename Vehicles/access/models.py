from django.db import models
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date


class Vehicles(models.Model):
    VEHICLE_CHOICES = [
        ("auto", "Auto"),
        ("motocicleta", "Motocicleta"),
        ("bicicleta", "Bicicleta"),
        ("camioneta", "Camioneta"),
        ("yate", "Yate"),
        ("velero", "Velero"),
        ("otro", "Otro"),
    ]

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_CHOICES)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, unique=True, primary_key=True)
    insurance_policy = models.OneToOneField(
        "InsurancePolicy", on_delete=models.CASCADE, related_name="vehicle"
    )

    def __str__(self):
        return f"{self.brand} {self.model} - {self.license_plate}"


class InsurancePolicy(models.Model):
    company_name = models.CharField(max_length=100)
    expiration_date = models.DateField()
