from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.conf import settings

# Create your models here.
class Facility(models.Model):
    facilityId = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 70, unique=True)

class Document(models.Model):
    name = models.CharField(max_length = 200)

class Service(Facility):
    type = models.CharField(max_length = 70, null = True)
    documents = models.ManyToManyField(Document, related_name = 'services', null = True)

class App(Facility):
    rate = models.IntegerField(default = 1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    description = models.TextField(null = True)
    cover = models.ImageField(blank=True, null=True)
    link = models.URLField(max_length=400, blank=True, null=True)
    englishName = models.CharField(max_length = 200, default='name')
    localHost = settings.LOCALHOST
    #coverURL = 'http://' + settings.LOCALHOST + '/'+settings.MEDIA_ROOT + cover.name +'/'



    