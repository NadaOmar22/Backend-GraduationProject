from django.contrib import admin
from .models import Citizen, AgencySupervisor, BranchSupervisor

admin.site.register(Citizen)
admin.site.register(AgencySupervisor)
admin.site.register(BranchSupervisor)

