from django.db import models
from FacilityApp.models import Service

class Branch(models.Model):
    name = models.CharField(max_length = 100)
    services = models.ManyToManyField(Service, related_name = 'branches', null = True)

class Agency (models.Model):
    name = models.CharField(max_length = 100)
    branches = models.ManyToManyField(Branch, related_name = 'govAgencies', null = True)

