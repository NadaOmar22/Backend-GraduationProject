from django.urls import re_path as url
from AuthApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    url('citizenRegister/',views.CitizenRegisterApi),
    url('citizenLogin/',views.CitizenLoginApi),
    url('citizenReviewsHistory/', views.CitizenReviewsHistoryApi),
    url('branchRegister/',views.BranchSupervisorRegisterApi),
    url('branchLogin/',views.BranchSupervisorLoginApi),
    url('agencyRegister/',views.AgencySupervisorRegisterApi),
    url('agencyLogin/',views.AgencySupervisorLoginApi), 
    url('editProfile/', views.CitizenEditProfileApi) ,  
] 
