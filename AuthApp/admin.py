from django.contrib import admin
from .models import Citizen, AgencySupervisor, BranchSupervisor
# Register your models here.
admin.site.register(Citizen)
admin.site.register(AgencySupervisor)
admin.site.register(BranchSupervisor)

