#from ModelApp.models import Review
from FacilityApp.models import Facility, App, Service
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import ServiceSerializer, DocumentSerializer
from AgencyApp.models import Branch

"""
@csrf_exempt
def GetFacilityReviewsApi(request):
    if request.method == 'GET':
        facility_data=JSONParser().parse(request)
        facility = Facility.objects.get(Name = facility_data['Name'])
        return JsonResponse (str(Review.objects.filter(Destination = facility).values()), safe=False)
    else:
       return JsonResponse ("Error: Wrong Method Type",safe=False)  
"""

@csrf_exempt   
def GetAppsAPI(request):
    if request.method == 'GET':
        return JsonResponse (str(App.objects.values()), safe=False)

@csrf_exempt   
def GetServicesForBranchAPI(request):
    if request.method == 'GET':
        requestData = JSONParser().parse(request)
        branchObj = Branch.objects.get(name = requestData['name'])   
        services = branchObj.services.all()
        serializer = ServiceSerializer(services, many=True)
        return JsonResponse (str(serializer.data), safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)    
    

@csrf_exempt   
def GetServicesWithSpecificTypeAPI(request):
    if request.method == 'GET':
        requestData = JSONParser().parse(request)
        services = Service.objects.filter(type = requestData['type'])   
        serializer = ServiceSerializer(services, many=True)
        return JsonResponse (str(serializer.data), safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)    
    
@csrf_exempt   
def GetDocumentsForServiceAPI(request):
    if request.method == 'GET':
        requestData = JSONParser().parse(request)
        serviceObj = Service.objects.get(Name = requestData['name'])   
        documents = serviceObj.Documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return JsonResponse (str(serializer.data), safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)