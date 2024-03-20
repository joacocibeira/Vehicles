import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from .models import Vehicles, InsurancePolicy
from datetime import datetime


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test_user", email="test@example.com", password="password"
    )


@pytest.fixture
def access_token(user):
    return str(AccessToken.for_user(user))


@pytest.fixture
def insurance_policy():
    # Create an insurance policy
    policy = InsurancePolicy.objects.create(
        company_name="Test Insurance", expiration_date=datetime(2024, 3, 20)
    )
    yield policy
    # Clean up after the test
    policy.delete()


@pytest.fixture
def vehicle(api_client, access_token, insurance_policy):
    # Create a vehicle with the insurance policy
    vehicle = Vehicles.objects.create(
        vehicle_type="auto",
        brand="Test Brand",
        model="Test Model",
        color="Test Color",
        license_plate="ABC-123",
        insurance_policy=insurance_policy,
    )
    return vehicle


@pytest.mark.django_db
def test_create_vehicle(api_client, access_token):
    data = {
        "vehicle_type": "auto",
        "brand": "Test Brand",
        "model": "Test Model",
        "color": "Test color",
        "license_plate": "ABC-123",
        "insurance_policy": {
            "id": 0,
            "company_name": "Test insurance",
            "expiration_date": "2024-03-20",
        },
    }

    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    # Make POST request
    response = api_client.post("/api/vehicles/", data, **headers, format="json")

    # Check if vehicle is created successfully
    assert response.status_code == 201
    assert Vehicles.objects.count() == 1
    assert Vehicles.objects.first().brand == "Test Brand"


@pytest.mark.django_db
def test_create_vehicle_should_fail(api_client, access_token):
    """This test should fail due to a wrong license plate format"""
    data = {
        "vehicle_type": "auto",
        "brand": "Test Brand",
        "model": "Test Model",
        "color": "Test color",
        "license_plate": "ABC123",
        "insurance_policy": {
            "id": 0,
            "company_name": "Test insurance",
            "expiration_date": "2024-03-20",
        },
    }

    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    # Make POST request
    response = api_client.post("/api/vehicles/", data, **headers, format="json")

    # Check errors
    assert response.status_code == 400


@pytest.mark.django_db
def test_retrieve_vehicle(api_client, access_token, vehicle):
    # Make GET request
    headers = {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}
    response = api_client.get(
        f"/api/vehicles/{vehicle.license_plate}/", **headers, format="json"
    )

    # Check if vehicle is retrieved successfully
    assert response.status_code == 200
    assert response.data["brand"] == "Test Brand"
    assert response.data["insurance_policy"]["company_name"] == "Test Insurance"


@pytest.mark.django_db
def test_update_vehicle(api_client, access_token, vehicle):
    # Prepare updated data
    updated_data = {
        "vehicle_type": "auto",
        "brand": "Updated Brand",
        "model": "Updated Model",
        "color": "Updated Color",
        "license_plate": "XYZ-789",
        "insurance_policy": {
            "company_name": "Test insurance",
            "expiration_date": "2024-03-20",
        },
    }
    headers = {
        "HTTP_AUTHORIZATION": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Make PUT request
    response = api_client.patch(
        f"/api/vehicles/{vehicle.license_plate}/",
        updated_data,
        **headers,
        format="json",
    )

    # Check if vehicle is updated successfully
    assert response.status_code == 200
    vehicle.refresh_from_db()
    assert vehicle.brand == "Updated Brand"
