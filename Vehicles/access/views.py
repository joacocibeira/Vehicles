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
        vehicle_type = self.request.query_params.get("vehicle_type")
        license_plate = self.request.query_params.get("license_plate")
        if vehicle_type is not None and license_plate is not None:
            queryset = queryset.filter(
                vehicle_type=vehicle_type, license_plate=license_plate
            )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a model instance by vehicle type and license plate instead of the
        PK
        """
        vehicle_type = request.query_params.get("vehicle_type")
        license_plate = request.query_params.get("license_plate")
        if not vehicle_type or not license_plate:
            return Response(
                {"error": "Vehicle type and license plate are required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = (
            self.get_queryset()
            .filter(vehicle_type=vehicle_type, license_plate=license_plate)
            .first()
        )
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(
                {"error": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND
            )
