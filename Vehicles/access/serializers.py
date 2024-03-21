from rest_framework import serializers
from .models import Vehicles, InsurancePolicy
import re
from django.utils import timezone


# Regex patterns for license plates for different vehicle types
LICENSE_PLATE_PATTERNS = {
    "auto": r"^[A-Z]{3}-\d{3}$",  # Example: ABC-123
    "motocicleta": r"^[A-Z0-9]{5}$",  # Example: ABC12
    "bicicleta": r"^[A-Z0-9]{4}$",  # Example: ABC1
    "camioneta": r"^[A-Z]{2}-\d{3}-[A-Z]{2}$",  # Example: AB-123-CD
    "yate": r"^[A-Z]{2}\d{4}$",  # Example: AB1234
    "velero": r"^[A-Z]{3}-\d{2}$",  # Example: ABC-12
    "otro": r".*",
}


class InsurancePolicySerializer(serializers.ModelSerializer):
    expiration_date = serializers.DateTimeField(
        required=False,
        allow_null=True,
        format="%d-%m-%Y",  # Specify the desired date format
        input_formats=["%d-%m-%Y"],  # Add the input format for parsing
    )

    def validate_expiration_date(self, value):
        today = timezone.now().date()
        if value and value.date() <= today + timezone.timedelta(days=30):
            raise serializers.ValidationError(
                "Insurance policy must expire at least a month from now"
            )
        return value

    def validate(self, data):
        # Ensure expiration date is in the desired format
        if "expiration_date" in data:
            data["expiration_date"] = data["expiration_date"].strftime("%d-%m-%Y")
        return data

    class Meta:
        model = InsurancePolicy
        fields = ["id", "company_name", "expiration_date"]


class VehiclesSerializer(serializers.ModelSerializer):
    insurance_policy = InsurancePolicySerializer()

    class Meta:
        model = Vehicles
        fields = [
            "vehicle_type",
            "brand",
            "model",
            "color",
            "license_plate",
            "insurance_policy",
        ]

        extra_kwargs = {
            "vehicle_type": {"required": True},
            "brand": {"required": True},
            "model": {"required": True},
            "color": {"required": True},
            "license_plate": {"required": True},
            "insurance_policy": {"required": True},
        }

    def create(self, validated_data):
        insurance_policy_data = validated_data.pop("insurance_policy")
        insurance_policy = InsurancePolicy.objects.create(**insurance_policy_data)
        vehicle = Vehicles.objects.create(
            insurance_policy=insurance_policy, **validated_data
        )
        return vehicle

    def update(self, instance, validated_data):
        insurance_policy_data = validated_data.pop("insurance_policy")
        insurance_policy = instance.insurance_policy

        instance.vehicle_type = validated_data.get(
            "vehicle_type", instance.vehicle_type
        )
        instance.brand = validated_data.get("brand", instance.brand)
        instance.model = validated_data.get("model", instance.model)
        instance.color = validated_data.get("color", instance.color)
        instance.license_plate = validated_data.get(
            "license_plate", instance.license_plate
        )
        instance.save()

        insurance_policy.company_name = insurance_policy_data.get(
            "company_name", insurance_policy.company_name
        )
        insurance_policy.expiration_date = insurance_policy_data.get(
            "expiration_date", insurance_policy.expiration_date
        )
        insurance_policy.save()

        return instance

    def validate_license_plate(self, value):
        return value.upper()

    def validate(self, data):
        pattern = LICENSE_PLATE_PATTERNS.get(data["vehicle_type"])

        if not re.match(pattern, data["license_plate"]):
            raise serializers.ValidationError(
                "Invalid license plate format for the given vehicle type."
            )
        return data


class VehicleUpdateSerializer(serializers.ModelSerializer):
    """Vehicle type and License plate fields are inmutable during the lifespan of a
    vehicle so we need a different serializer for partial updates"""

    insurance_policy = InsurancePolicySerializer(required=False)

    class Meta:
        model = Vehicles
        fields = [
            "brand",
            "model",
            "color",
            "insurance_policy",
        ]

    def update(self, instance, validated_data):
        # Retrieve insurance_policy data if present in validated_data
        insurance_policy_data = validated_data.pop("insurance_policy", None)

        # Update vehicle fields
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # Update insurance_policy fields if data is provided
        if insurance_policy_data:
            insurance_policy = instance.insurance_policy
            for key, value in insurance_policy_data.items():
                setattr(insurance_policy, key, value)
            insurance_policy.save()

        instance.save()
        return instance
