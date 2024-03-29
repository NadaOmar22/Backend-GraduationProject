from django.db import models
from django.contrib.auth.hashers import make_password
from AgencyApp.models import Branch, Agency

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)   
    password = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        if not self.pk: # check if the object is being created for the first time
            self.password = make_password(self.password) # encrypt the password
        super(User, self).save(*args, **kwargs)
    

class Citizen(User):
   nationalId = models.CharField(max_length=14, null=True, unique=True)
   email = models.EmailField(max_length=50, default='test@example.com', unique=True)
   phoneNumber = models.CharField(max_length=11)

   
   
class GovSupervisor(User):
    govId = models.CharField(max_length=100, unique=True)
    supervisionType = models.CharField(max_length=100)
    isApproved = models.BooleanField(default=False, null=True)

class BranchSupervisor(GovSupervisor):
    branch =  models.OneToOneField(Branch, on_delete=models.CASCADE, null=True)
    branchName = models.CharField(max_length=100, null=True)
    
class AgencySupervisor(GovSupervisor):
    agency = models.OneToOneField(Agency, on_delete=models.CASCADE, null=True)
    agencyName = models.CharField(max_length=100, null=True)

    
 