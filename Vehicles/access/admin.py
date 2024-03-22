from django.contrib import admin

from .models import Vehicles, InsurancePolicy

# Register your models here.
admin.site.register(Vehicles)
admin.site.register(InsurancePolicy)
