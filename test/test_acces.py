import pytest
from test.factories import VehicleFactory
from django.urls import reverse
from freezegun import freeze_time
from Vehicles.access.models import Vehicles
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db()
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


@pytest.mark.django_db()
def test_vehicle_retrieve(user, api_client):
    vehicle = VehicleFactory.create()

    # Obtain the access token
    login_url = reverse("token_obtain_pair")
    login_data = {"username": user.username, "password": "test_password"}
    response = api_client.post(path=login_url, data=login_data)
    access_token = response.data["access"]

    # Set authorization header with the access token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Make a GET request to the vehicles list endpoint
    list_url = reverse("vehicles-list") + f"{vehicle.license_plate}/"
    response = api_client.get(path=list_url)

    # Assert statements or other test logic here
    assert response.status_code == 200


@pytest.mark.django_db()
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


@pytest.mark.django_db()
@freeze_time("2024-01-01")
def test_vehicle_create_should_fail(user, api_client):
    """The insurance policy of the vehicle must have at least one month left to expire"""

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
            "expiration_date": "2023-12-31",
        },
    }

    # Make a POST request to create a new vehicle
    create_url = reverse("vehicles-list")
    response = api_client.post(path=create_url, data=new_vehicle_data, format="json")

    # Assert statements
    assert (
        response.status_code == 400
    )  # Check that the response status is 201 (Created)

    with pytest.raises(ObjectDoesNotExist):
        Vehicles.objects.get(license_plate="ABC-123")


@pytest.mark.django_db()
def test_vehicle_delete(user, api_client):
    vehicle = VehicleFactory.create()

    # Obtain the access token
    login_url = reverse("token_obtain_pair")
    login_data = {"username": user.username, "password": "test_password"}
    response = api_client.post(path=login_url, data=login_data)
    access_token = response.data["access"]

    # Set authorization header with the access token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Make a GET request to the vehicles list endpoint
    list_url = reverse("vehicles-list") + f"{vehicle.license_plate}/"
    response = api_client.delete(path=list_url)

    assert response.status_code == 204

    with pytest.raises(ObjectDoesNotExist):
        Vehicles.objects.get(license_plate=vehicle.license_plate)


@pytest.mark.django_db()
def test_vehicle_update(user, api_client):
    vehicle = VehicleFactory.create()

    # Obtain the access token
    login_url = reverse("token_obtain_pair")
    login_data = {"username": user.username, "password": "test_password"}
    response = api_client.post(path=login_url, data=login_data)
    access_token = response.data["access"]

    # Set authorization header with the access token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # Make a GET request to the vehicles list endpoint
    list_url = reverse("vehicles-list") + f"{vehicle.license_plate}/"

    update_data = {"brand": "Volkswagen", "model": "gol", "color": "gray"}
    response = api_client.patch(path=list_url, data=update_data)

    assert response.status_code == 200

    modified_vehicle = Vehicles.objects.get(license_plate=vehicle.license_plate)

    assert modified_vehicle.model == "gol"
