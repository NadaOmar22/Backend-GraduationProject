from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    UserId = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)   
    Password = models.CharField(max_length=128)
    

class Citizen(User):
   NationalId = models.CharField(max_length=14, null=True)
   Email = models.EmailField(max_length=50, default='test@example.com', unique=True)
   PhoneNumber = models.CharField(max_length=11)
   Gender = models.CharField(max_length=100, default='male')
   
class GovSupervisor(User):
    GovId = models.CharField(max_length=100, unique=True)
    GovAgencyName = models.CharField(max_length=100)

class BranchSupervisor(GovSupervisor):
    BranchName = models.CharField(max_length=100, unique=True)

class AgencySupervisor(GovSupervisor):
    AgencyName = models.CharField(max_length=100, unique=True)

 