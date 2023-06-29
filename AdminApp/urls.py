from django.urls import re_path as url
from AdminApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    url('administratorLogin/',views.AdministratorLoginApi),
    url('getAllUnapprovedAgencySupervisors/', views.GetAllUnapprovedAgencySupervisorsApi),
    url('getAllUnapprovedBranchSupervisors/', views.GetAllUnapprovedBranchSupervisorsApi),
    url('deleteAgencySupervisorFromDatabase/', views.DeleteAgencySupervisorFromDatabaseApi),
    url('deleteBranchSupervisorFromDatabase/', views.DeleteBranchSupervisorFromDatabaseApi),
    url('approveAgencySupervisor/', views.ApproveAgencySupervisorApi),
    url('approveBranchSupervisor/', views.ApproveBranchSupervisorApi),
    url('createAgency/', views.CreateAgencyApi),
    url('addApp/', views.AddAppApi),
    url('deleteApp/', views.DeleteAppApi),
] 
