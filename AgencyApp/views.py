from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import BranchSerializer, AgencySerializer
from FacilityApp.models import Service
from AuthApp.models import BranchSupervisor
from rest_framework.parsers import JSONParser
from AgencyApp.models import Branch, Agency
from django.core import serializers


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

@csrf_exempt 
def GetAgenciesForAdminApi(request):
    if request.method == 'POST':
        agencies = Agency.objects.all()
        response = []
        for agency in agencies:
            agencyData = AgencySerializer(agency)
            #agencyData2 = agencyData.data
            response.append(agencyData.data)
            """branchNames = set()
            serviceNames = set()
            for branch in agencyData2['branches']:
                branchName = branch['name']
                branchNames.add(branchName)
                for service in branch['services']:
                    serviceNames.add(service['name'])
            newAgencyData = {
                "agencyName": agencyData2['name'],
                "branches": list(branchNames),
                "services": list(serviceNames)
            }
            response.append(newAgencyData)"""
    return JsonResponse(response, safe=False)

@csrf_exempt 
def UpdateBranchServicesApi(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        branchSupervisor = BranchSupervisor.objects.get(govId = request_data['govId'])
        servicesObj = []
        for serviceName in request_data['services']:
            service = Service.objects.get(name = serviceName)
            servicesObj.append(service)
        branchSupervisor.branch.services.set(servicesObj)
        return JsonResponse("new services add", safe=False)

    return JsonResponse("wrong method type", safe=False)
        

@csrf_exempt 
def AddBranchApi(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
    
        branchName = request_data['branchName'] + ' ' + request_data['agencyName']
        if Branch.objects.filter(name=branchName).exists():
            return JsonResponse("Branch already exists!", safe=False) 

        location = request_data['location']
        agencyObj = Agency.objects.get(name = request_data['agencyName'])
        
        if branchName and location:
            newBranch = Branch(name=branchName, location=location)
            newBranch.save()
            agencyObj.branches.add(newBranch)
    
            return JsonResponse("Branch created successfully", safe=False)
        else:
            return JsonResponse("Name and location are required fields", safe=False)
    else:
        return JsonResponse("error': 'Method not allowed" ,safe=False)    


        
@csrf_exempt 
def DeleteBranchApi(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        if request_data:
            branch = Branch.objects.get(name=request_data['branchName'])
            branch.delete()
            return JsonResponse("Branch deleted successfully", safe=False)
        return JsonResponse("branch name is required", safe=False)
    return JsonResponse("error': 'Method not allowed" ,safe=False)    



