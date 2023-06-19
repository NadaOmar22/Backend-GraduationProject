from django.urls import re_path as url
from AuthApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    url('citizenSignup/',views.CitizenSignupApi),
    url('citizenLogin/',views.CitizenLoginApi),
    url('citizenReviewsHistory/', views.CitizenReviewsHistoryApi),
    url('branchSignup/',views.BranchSupervisorSignupApi),
    url('branchLogin/',views.BranchSupervisorLoginApi),
    url('agencySignup/',views.AgencySupervisorSignupApi),
    url('agencyLogin/',views.AgencySupervisorLoginApi), 
    url('editProfile/', views.CitizenEditProfileApi),
    url('addreview/', views.CitizenAddReviewApi), 
    url('serviceReviewsFilteredByYear/', views.ServiceReviewsFilteredByYearApi),
    url('branchReviewsFilteredByYear/', views.BranchReviewsFilteredByYearApi)
] 
