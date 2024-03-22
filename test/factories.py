import factory
from Vehicles.access import models
import datetime


class InsurancePolicyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.InsurancePolicy

    company_name = factory.Faker("company")
    expiration_date = factory.LazyFunction(
        lambda: datetime.date.today() + datetime.timedelta(days=30)
    )


class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vehicles

    vehicle_type = "auto"
    brand = factory.Faker("company")
    model = factory.Faker("word")
    color = factory.Faker("color_name")
    license_plate = factory.Sequence(lambda n: f"ABC-{n:03}")
    insurance_policy = factory.SubFactory(InsurancePolicyFactory)
