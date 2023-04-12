from django.db import models
from AuthApp.models import Citizen
from FacilityApp.models import Facility

class Review(models.Model):
    ReviewId = models.AutoField(primary_key=True)
    Source = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True, max_length = 300)
    Destination = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, max_length = 300)
    Description = models.CharField(max_length = 300)
    State = models.CharField(max_length = 100)
    Polarity = models.CharField(max_length = 20)