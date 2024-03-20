from rest_framework import serializers
from .models import Vehicles, InsurancePolicy


class InsurancePolicySerializer(serializers.ModelSerializer):
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
