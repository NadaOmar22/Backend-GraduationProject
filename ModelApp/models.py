from django.db import models
from AuthApp.models import Citizen

class Review(models.Model):
    ReviewId = models.AutoField(primary_key=True)
    Source = models.ForeignKey(Citizen, on_delete=models.CASCADE, null=True, max_length = 300)
    Destination = models.CharField(max_length = 300)
    Description = models.CharField(max_length = 300)
    State = models.CharField(max_length = 100)