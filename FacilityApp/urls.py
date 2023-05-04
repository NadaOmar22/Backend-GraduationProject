from django.urls import re_path as url , path
from django.conf.urls.static import static
from django.conf import settings
from FacilityApp import views


urlpatterns=[
   #url('facilityReviews/', views.GetFacilityReviewsApi),
   url('allApps/', views.GetAppsAPI), 
   url('servicesForBranch/', views.GetServicesForBranchAPI),  
   url('documentsForService/', views.GetDocumentsForServiceAPI),   
   url('servicesByType/', views.GetServicesWithSpecificTypeAPI),
   url('addDocument/', views.AddDocumentAPI),
   url('addService/', views.AddServiceAPI),
   path('media/covers/<path:filename>/', views.ServeImage),
] 

