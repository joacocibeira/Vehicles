from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vehicles
from .serializers import VehiclesSerializer


class VehiclesViewSet(viewsets.ModelViewSet):

    queryset = Vehicles.objects.all()
    serializer_class = VehiclesSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned vehicles to a given type and
        license plate by filtering against query parameters in the URL.
        """
        queryset = Vehicles.objects.all()
        license_plate = self.request.query_params.get("license_plate")
        if license_plate:
            queryset = queryset.filter(license_plate=license_plate)
        return queryset
