from django.db import models
from FacilityApp.models import Service

class Branch(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100, null=True)
    services = models.ManyToManyField(Service, related_name = 'branches', null = True)

class Agency (models.Model):
    name = models.CharField(max_length = 100)
    allServices = models.ManyToManyField(Service, related_name = 'agency', null = True)
    branches = models.ManyToManyField(Branch, related_name = 'govAgencies', null = True)

