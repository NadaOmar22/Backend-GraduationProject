from django.urls import re_path as url
from django.conf.urls.static import static
from django.conf import settings
from FacilityApp import views


urlpatterns=[
   #url('facilityReviews/', views.GetFacilityReviewsApi),
   url('allApps/', views.GetAppsAPI), 
   url('servicesForBranch/', views.GetServicesForBranchAPI),  
   url('documentsForService/', views.GetDocumentsForServiceAPI),   
   url('servicesByType/', views.GetServicesWithSpecificTypeAPI),
] 