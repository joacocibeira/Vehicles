from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vehicles
from .serializers import VehiclesSerializer, VehicleUpdateSerializer


class VehiclesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Vehicles.objects.all()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return VehicleUpdateSerializer
        return VehiclesSerializer

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
