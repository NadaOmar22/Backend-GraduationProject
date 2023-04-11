from django.db import models

# Create your models here.
class Facility(models.Model):
    FacilityId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length = 70)

class Service(Facility):
    type = models.CharField(max_length = 70)

class App(Facility):
    rate = models.IntegerField()
    