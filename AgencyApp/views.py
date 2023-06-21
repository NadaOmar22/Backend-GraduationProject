from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import BranchSerializer, AgencySerializer
from FacilityApp.models import Service
from rest_framework.parsers import JSONParser
from AgencyApp.models import Branch, Agency


@csrf_exempt   
def GetBranchesForAgencyApi(request):
    if request.method == 'POST':
        agencyData = JSONParser().parse(request)
        agencyObj = Agency.objects.get(name = agencyData['agencyName'])   
        branches = agencyObj.branches.all()
        response = []
        for branch in branches:
            response.append(branch.name)
        return JsonResponse (response, safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)

@csrf_exempt 
def GetAgenciesApi(request):
    if request.method == 'GET':
        agencies = Agency.objects.all()  
        response = []
        for agency in agencies:
            response.append(agency.name)
        return JsonResponse (response, safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)
