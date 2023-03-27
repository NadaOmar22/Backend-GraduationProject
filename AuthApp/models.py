from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    UserId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=50, default='test@example.com', unique=True)
    Password = models.CharField(max_length=128)
    Gender = models.CharField(max_length=100, default='male')

    #def save(self, *args, **kwargs):
        #self.Password = make_password(self.Password)
        #super().save(*args, **kwargs)

class Citizen(User):
   PhoneNumber = models.CharField(max_length=12)

class GovSupervisor(User):
    GovId = models.CharField(max_length=100, unique=True)
    GovAgencyName = models.CharField(max_length=100)

class BranchSupervisor(GovSupervisor):
    BranchName = models.CharField(max_length=100, unique=True)

class AgencySupervisor(GovSupervisor):
    AgencyName = models.CharField(max_length=100, unique=True)
