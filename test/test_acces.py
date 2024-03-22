import pytest
from test.factories import VehicleFactory
from django.urls import reverse
from freezegun import freeze_time
from datetime import datetime
from Vehicles.access.models import Vehicles


def test_vehicle_list(user, api_client):
    # Build 5 vehicle instances using Factory Boy
    vehicles = VehicleFactory.create_batch(5)

    # Obtain the access token
    login_url = reverse("token_obtain_pair")
    login_data = {"username": user.username, "password": "test_password"}
    response = api_client.post(path=login_url, data=login_data)
    access_token = response.data["access"]

    # Set authorization header with the access token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Make a GET request to the vehicles list endpoint
    list_url = reverse("vehicles-list")
    response = api_client.get(path=list_url)

    # Assert statements or other test logic here
    assert response.status_code == 200
    assert response.data["count"] == 5  # Check that the response contains 5 vehicles


@freeze_time("2024-01-01")
def test_vehicle_create(user, api_client):

    # Obtain the access token
    login_url = reverse("token_obtain_pair")
    login_data = {"username": user.username, "password": "test_password"}
    response = api_client.post(path=login_url, data=login_data)
    access_token = response.data["access"]

    # Set authorization header with the access token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Data for creating a new vehicle
    new_vehicle_data = {
        "vehicle_type": "auto",
        "brand": "Toyota",
        "model": "Corolla",
        "color": "Red",
        "license_plate": "ABC-123",
        "insurance_policy": {
            "company_name": "Insurance Corp",
            "expiration_date": "2025-12-31",
        },
    }

    # Make a POST request to create a new vehicle
    create_url = reverse("vehicles-list")
    response = api_client.post(path=create_url, data=new_vehicle_data, format="json")

    # Assert statements
    assert (
        response.status_code == 201
    )  # Check that the response status is 201 (Created)

    # Query the Vehicles model to retrieve the created vehicle
    created_vehicle = Vehicles.objects.get(license_plate="ABC-123")

    assert created_vehicle is not None
