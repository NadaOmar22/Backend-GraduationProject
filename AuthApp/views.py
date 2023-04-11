from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from AuthApp.models import Citizen, AgencySupervisor, BranchSupervisor
from AuthApp.serializers import CitizenRegisterSerializer, BranchSupervisorRegisterSerializer, AgencySupervisorRegisterSerializer
from django.core.files.storage import default_storage
from ModelApp.models import Review


#ASupervisor  Citizen  Branch
# Create your views here.
@csrf_exempt
def CitizenRegisterApi(request):
    if request.method == 'POST':
        citizen_data=JSONParser().parse(request)
        citizen_serializer = CitizenRegisterSerializer(data=citizen_data)
        print(citizen_data)
        print(citizen_serializer)
        if citizen_serializer.is_valid():
            citizen_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse("Failed to Add.", safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenLoginApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        if Citizen.objects.filter(Email=citizen_data['Email'] , Password=citizen_data['Password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid name or password.",safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenEditProfileApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        CurrentCitizen = Citizen.objects.get(NationalId=citizen_data['NationalId'])
        CurrentCitizen.Name = citizen_data['Name']
        CurrentCitizen.Email = citizen_data['Email']
        CurrentCitizen.Password = citizen_data['Password']
        CurrentCitizen.PhoneNumber = citizen_data['PhoneNumber']
        CurrentCitizen.save()
        return JsonResponse("Data updated Successfully!!" , safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenReviewsHistoryApi(request):
    if request.method == 'GET':
        citizen_data=JSONParser().parse(request)
        CurrentCitizen = Citizen.objects.get(NationalId=citizen_data['NationalId'])
        return JsonResponse (str(Review.objects.filter(Source = CurrentCitizen).values()), safe=False)
    else:
       return JsonResponse ("Error: Wrong Method Type",safe=False)   


# GovSupervisor Register and Login
@csrf_exempt
def BranchSupervisorRegisterApi(request):
    branchSupervisor_data = JSONParser().parse(request)
    branchSupervisor_serializer = BranchSupervisorRegisterSerializer(data = branchSupervisor_data)
    if branchSupervisor_serializer.is_valid():
        branchSupervisor_serializer.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    return JsonResponse("Failed to Add.",safe=False)

@csrf_exempt
def BranchSupervisorLoginApi(request):
    if request.method == 'POST':
        branchSupervisor_data = JSONParser().parse(request)
        if BranchSupervisor.objects.filter(Email = branchSupervisor_data['Email'] , Password=branchSupervisor_data['Password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.",safe=False)
    

@csrf_exempt
def AgencySupervisorRegisterApi(request):
    agencySupervisor_data = JSONParser().parse(request)
    agencySupervisor_serializer = AgencySupervisorRegisterSerializer(data = agencySupervisor_data)
    if agencySupervisor_serializer.is_valid():
        agencySupervisor_serializer.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    return JsonResponse("Failed to Add.",safe=False)

@csrf_exempt
def AgencySupervisorLoginApi(request):
    if request.method == 'POST':
        agencySupervisor_data = JSONParser().parse(request)
        if AgencySupervisor.objects.filter(Email = agencySupervisor_data['Email'] , Password=agencySupervisor_data['Password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.",safe=False)
    
