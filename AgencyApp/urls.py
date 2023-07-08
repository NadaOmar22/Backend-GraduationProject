from django.urls import re_path as url
from django.conf.urls.static import static
from django.conf import settings
from AgencyApp import views


urlpatterns=[
   url('getBranchesForAgency/', views.GetBranchesForAgencyApi), 
   url('getAgencies/', views.GetAgenciesApi),
   url('getAgenciesForAdmin/', views.GetAgenciesForAdminApi),
   url('updateBranchServices/', views.UpdateBranchServicesApi),
   url('addBranch/', views.AddBranchApi),
   url('deleteBranch/', views.DeleteBranchApi),
] 