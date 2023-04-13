from django.urls import re_path as url
from AdminApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    url('administratorLogin/',views.AdministratorLoginApi)
] 
