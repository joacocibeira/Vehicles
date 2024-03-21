import pytest
from test.factories import VehicleFactory


def test_vehicle_list():
    vehicle = VehicleFactory.build()
    print(vehicle)
    assert 1 == 1
