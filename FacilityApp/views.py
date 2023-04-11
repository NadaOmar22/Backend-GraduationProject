from django.shortcuts import render
from ModelApp.models import Review
from FacilityApp.models import Facility
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def GetFacilityReviewsApi(request):
    if request.method == 'GET':
        facility_data=JSONParser().parse(request)
        facility = Facility.objects.get(Name=facility_data['Name'])
        return JsonResponse (str(Review.objects.filter(Destination = facility).values()), safe=False)
    else:
       return JsonResponse ("Error: Wrong Method Type",safe=False)  

