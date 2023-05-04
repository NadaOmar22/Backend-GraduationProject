from django.db import models
from AuthApp.models import Citizen
from FacilityApp.models import Facility

"""
class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    source = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True, max_length = 300)
    destination = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, max_length = 300)
    description = models.CharField(max_length = 300)
    state = models.CharField(max_length = 100)
    polarity = models.CharField(max_length = 20)
"""