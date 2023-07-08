import json
from django.shortcuts import render
from .models import Administrator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from AuthApp.models import AgencySupervisor, BranchSupervisor
from FacilityApp.models import Document, Service, App
from AgencyApp.models import Agency, Branch
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


@csrf_exempt
def AdministratorLoginApi(request):
    if request.method == 'POST':
        administrator_data = JSONParser().parse(request)
        obj = Administrator.load()
        if obj.username == administrator_data['username'] and obj.password  == administrator_data['password']:
            return JsonResponse("LoggedIn Successfully!!", safe=False)
        return JsonResponse("Invalid username or password.",safe=False)     

@csrf_exempt
def GetAllUnapprovedAgencySupervisorsApi(request):
    if request.method=='POST':
        agencySupervisorObjects = AgencySupervisor.objects.filter(isApproved = False)
        agencySupervisorsList = []
        for agencySupervisor in agencySupervisorObjects:
            agencySupervisorData = {
                "name": agencySupervisor.name,
                "govId":agencySupervisor.govId
            }
            agencySupervisorsList.append(agencySupervisorData)
        return JsonResponse(agencySupervisorsList,safe=False)

@csrf_exempt
def GetAllUnapprovedBranchSupervisorsApi(request):
    if request.method=='POST':
        branchSupervisorObjects = BranchSupervisor.objects.filter(isApproved = False)
        branchSupervisorsList = []
        for agencySupervisor in branchSupervisorObjects:
            branchSupervisorData = {
                "name": agencySupervisor.name,
                "govId":agencySupervisor.govId
            }
            branchSupervisorsList.append(branchSupervisorData)
        return JsonResponse(branchSupervisorsList,safe=False)
    
@csrf_exempt
def DeleteAgencySupervisorFromDatabaseApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            agencySupervisor = AgencySupervisor.objects.get(govId = request_data['govId'])
            agencySupervisor.delete()
        except AgencySupervisor.DoesNotExist:
            return JsonResponse("AgencySupervisor Not Found!!",safe=False) 
        return JsonResponse("AgencySupervisor Deleted Successfully!!",safe=False)

@csrf_exempt
def DeleteBranchSupervisorFromDatabaseApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            branchSupervisor = BranchSupervisor.objects.get(govId = request_data['govId'])
            branchSupervisor.delete()
        except BranchSupervisor.DoesNotExist:
            return JsonResponse("BranchSupervisor Not Found!!",safe=False) 
        return JsonResponse("BranchSupervisor Deleted Successfully!!",safe=False)
    
@csrf_exempt
def ApproveAgencySupervisorApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            agencySupervisor = AgencySupervisor.objects.get(govId = request_data['govId'])
            agencySupervisor.isApproved = True
            agencySupervisor.save()
        except AgencySupervisor.DoesNotExist:
            return JsonResponse("AgencySupervisor Not Found!!",safe=False) 
        return JsonResponse("AgencySupervisor Approved Successfully!!",safe=False)

@csrf_exempt
def ApproveBranchSupervisorApi(request):
    if request.method=='POST':
        request_data = JSONParser().parse(request)
        try:
            branchSupervisor = BranchSupervisor.objects.get(govId = request_data['govId'])
            branchSupervisor.isApproved = True
            branchSupervisor.save()
        except BranchSupervisor.DoesNotExist:
            return JsonResponse("BranchSupervisor Not Found!!",safe=False) 
        return JsonResponse("BranchSupervisor Approved Successfully!!",safe=False)
 
@csrf_exempt
def CreateAgencyApi(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        agencyName = data['agencyName']
        agency_exists = Agency.objects.filter(name=agencyName).exists()
        if agency_exists:
            return JsonResponse("agency already exists", safe=False)
        else:
            new_agency = Agency(name=agencyName)
            branchName = data['branchName'] + ' ' + agencyName
            branchLocation = data['branchLocation']
            new_agency.save()
            new_branch = Branch(name=branchName, location=branchLocation)
            new_branch.save()
            new_agency.branches.add(new_branch)
            new_agency.save()
            return JsonResponse("agency created sucessfully!!", safe=False)
    else:
        return JsonResponse("wrong method type", safe=False)


@csrf_exempt
def AddAppApi(request):
    if request.method=='POST':
        app_data = request.POST
        cover_file = request.FILES.get('cover', None)

        if not cover_file:
            return JsonResponse("No cover file provided", safe=False)
        
        if App.objects.filter(name=app_data["name"]).exists():
            return JsonResponse("App already exists!!" , safe=False)

        newAPP = App(
                name = app_data["name"],
                rate = app_data["rate"],
                englishName = app_data["engName"],
                link = app_data["link"],
                description = app_data["description"],
                cover = cover_file
        )
        newAPP.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    

@csrf_exempt
def DeleteAppApi(request):
    if request.method=='POST':
        app_data = JSONParser().parse(request)
        try:
            app_obj = App.objects.filter(name = app_data["name"])
            app_obj.delete()
        except App.DoesNotExist:
            return JsonResponse("app Not Found!!",safe=False) 
        return JsonResponse("App Deleted Successfully!!", safe=False)