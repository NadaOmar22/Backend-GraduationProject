from django.contrib import admin
from .models import Facility, Service, App


# Register your models here.
admin.site.register(Facility)
admin.site.register(Service)
admin.site.register(App)
