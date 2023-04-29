from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)   
    password = models.CharField(max_length=128)
    

class Citizen(User):
   nationalId = models.CharField(max_length=14, null=True)
   email = models.EmailField(max_length=50, default='test@example.com', unique=True)
   phoneNumber = models.CharField(max_length=11)
   
class GovSupervisor(User):
    govId = models.CharField(max_length=100, unique=True)
    supervisionType = models.CharField(max_length=100)

class BranchSupervisor(GovSupervisor):
    branchName = models.CharField(max_length=100, unique=True)

class AgencySupervisor(GovSupervisor):
    agencyName = models.CharField(max_length=100, unique=True)

 