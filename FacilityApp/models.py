from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Facility(models.Model):
    facilityId = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 70)

class Document(models.Model):
    name = models.CharField(max_length = 200)

class Service(Facility):
    type = models.CharField(max_length = 70)
    documents = models.ManyToManyField(Document, related_name = 'services', null = True)

class App(Facility):
    rate = models.IntegerField(default = 1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    