from django.views.decorators.csrf import csrf_exempt
from FacilityApp.models import Facility
from FacilityApp.serializers import DocumentSerializer
from AgencyApp.models import Branch
from AgencyApp.serializers import BranchSerializer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from ModelApp.models import Review
from AgencyApp.models import Agency
from AuthApp.models import Citizen, AgencySupervisor, BranchSupervisor
from ModelApp.MachineModel.sentimentanalysis_gpmodel import prediction
from AuthApp.serializers import CitizenSignupSerializer, BranchSupervisorSignupSerializer, AgencySupervisorSignupSerializer


@csrf_exempt
def CitizenSignupApi(request):
    if request.method == 'POST':
        citizen_data=JSONParser().parse(request)
        citizen_serializer = CitizenSignupSerializer(data=citizen_data)
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
        if Citizen.objects.filter(email=citizen_data['email'] , password=citizen_data['password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.",safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenEditProfileApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        CurrentCitizen = Citizen.objects.get(email=citizen_data['email'])
        CurrentCitizen.name = citizen_data['name']
        CurrentCitizen.email = citizen_data['email']
        CurrentCitizen.password = citizen_data['password']
        CurrentCitizen.phoneNumber = citizen_data['phoneNumber']
        CurrentCitizen.save()
        return JsonResponse("Data updated Successfully!!" , safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)


@csrf_exempt
def GetCitizenByEmailApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        requiredCitizen = Citizen.objects.get(email=citizen_data['email'])
        response = {
            "name": requiredCitizen.name,
            "email": requiredCitizen.email,
            "phoneNumber": requiredCitizen.phoneNumber,
            "password": requiredCitizen.password,
            "nationalId" : requiredCitizen.nationalId
        } 
        return JsonResponse(response,safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenAddReviewApi(request):
    if request.method == 'POST':
        review_data=JSONParser().parse(request)
        citizen = Citizen.objects.get(email=review_data['email'])
        facility = Facility.objects.get(name=review_data['destination'])
        branch = Branch.objects.get(name=review_data['relatedBranch'])

        newReview = Review()

        newReview.source = citizen
        newReview.destination = facility
        newReview.description = review_data['description']
        newReview.relatedBranch = branch
        newReview.state = review_data['state']
        newReview.polarity = prediction(review_data['description'])[0]

        newReview.save()
        return JsonResponse("Added Successfully!!", safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def CitizenReviewsHistoryApi(request):
    if request.method == 'POST':
        citizen_data=JSONParser().parse(request)
        currentCitizen = Citizen.objects.get(email=citizen_data['email'])
        reviews = Review.objects.filter(source = currentCitizen)
        response = []
        for review in reviews:
            dict = {
                "description": review.description,
                "state": review.state,
                "destination" : review.destination.name
            }
            response.append(dict)
        return JsonResponse (response , safe=False)
    else:
       return JsonResponse ("Error: Wrong Method Type",safe=False)   

# GovSupervisor Register and Login
@csrf_exempt
def BranchSupervisorSignupApi(request):
    branchSupervisor_data = JSONParser().parse(request)
    branchSupervisor_serializer = BranchSupervisorSignupSerializer(data = branchSupervisor_data)
    if branchSupervisor_serializer.is_valid():
        branchSupervisor_serializer.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    return JsonResponse("Failed to Add.",safe=False)

@csrf_exempt
def BranchSupervisorLoginApi(request):
    if request.method == 'POST':
        branchSupervisor_data = JSONParser().parse(request)
        if BranchSupervisor.objects.filter(govId = branchSupervisor_data['govId'] , password=branchSupervisor_data['password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid Id or password.",safe=False)
    
@csrf_exempt
def GetBranchSupervisorByIdApi(request):
    if request.method=='POST':
        branchSuper_data=JSONParser().parse(request)
        requiredBranchSupervisior = BranchSupervisor.objects.get(govId=branchSuper_data['govId'])
        response = {
            "name": requiredBranchSupervisior.name,
            "govId": requiredBranchSupervisior.govId,
            "password": requiredBranchSupervisior.password,
            "branchName" : requiredBranchSupervisior.branchName,
            "supervisionType": requiredBranchSupervisior.supervisionType
        } 
        return JsonResponse(response,safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)
    

@csrf_exempt
def AgencySupervisorSignupApi(request):
    agencySupervisor_data = JSONParser().parse(request)
    agencySupervisor_serializer = AgencySupervisorSignupSerializer(data = agencySupervisor_data)
    if agencySupervisor_serializer.is_valid():
        agencySupervisor_serializer.save()
        return JsonResponse("Added Successfully!!" , safe=False)
    return JsonResponse("Failed to Add.",safe=False)

@csrf_exempt
def AgencySupervisorLoginApi(request):
    if request.method == 'POST':
        agencySupervisor_data = JSONParser().parse(request)
        if AgencySupervisor.objects.filter(govId = agencySupervisor_data['govId'] , password=agencySupervisor_data['password']):
            return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.",safe=False)

@csrf_exempt
def GetAgencySupervisorByIdApi(request):
    if request.method=='POST':
        agencySuper_data=JSONParser().parse(request)
        requiredBranchSupervisior = AgencySupervisor.objects.get(govId=agencySuper_data['govId'])
        response = {
            "name": requiredBranchSupervisior.name,
            "govId": requiredBranchSupervisior.govId,
            "password": requiredBranchSupervisior.password,
            "agencyName" : requiredBranchSupervisior.agencyName,
            "supervisionType": requiredBranchSupervisior.supervisionType
        } 
        return JsonResponse(response,safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)

@csrf_exempt
def GetTotalNumberOfEachUserApi(request):
    if request.method=='POST':
        citizenObjects = Citizen.objects.all()
        branchSupervisorObjects = BranchSupervisor.objects.all()
        agencySupervisorObjects = AgencySupervisor.objects.all()

        response = {
            "citizensCount": len(citizenObjects),
            "branchSupervisorsCount": len(branchSupervisorObjects),
            "agencySupervisorsCount": len(agencySupervisorObjects)
        }
    return JsonResponse(response,safe=False)

@csrf_exempt
def GetAllAgencyServicesForBranchSupervisor(request):
    if request.method == 'POST':
        request_data=JSONParser().parse(request)
        branchSupervisor = BranchSupervisor.objects.get(govId = request_data['govId'])
        targetBranch = Branch.objects.get(name = branchSupervisor.branch.name)
        agencies = Agency.objects.all()
        targetAgency = Agency()
        found = False
        for agency in agencies:
            for agencyBranch in agency.branches.all():
                if agencyBranch == targetBranch:
                    targetAgency = agency
                    found = True
                    break
            if (found == True):
                break
        
        agencyServices  = []
        branchServices = []
        for service in targetBranch.services.all():
            branchServices.append(service.name)
        
        for service in targetAgency.allServices.all():
            if(service.name not in branchServices):
                agencyServices.append(service.name)

        if(len(agencyServices) == 0):
            return JsonResponse("services list in agency is empty", safe=False)
        if(len(branchServices) == 0):
            return JsonResponse("services list in branch is empty", safe=False)
        
        response = {
           "agencyServices": agencyServices,
           "branchServices": branchServices
        }

        return JsonResponse(response, safe=False)
    return JsonResponse("wrong method type", safe=False)
        
@csrf_exempt
def GetAllAgencyServicesForAgencySupervisor(request):
    if request.method == 'POST':
        request_data=JSONParser().parse(request)
        agencySupervisor = AgencySupervisor.objects.get(govId = request_data['govId'])
        services = agencySupervisor.agency.allServices.all()
        branches = agencySupervisor.agency.branches.all()
        
        agencyServices  = []
        for service in services:
            branchesForService = []
            for branch in branches:
                if branch.services.all().filter(name=service.name).exists():
                    branchesForService.append(branch.name)
            documentsList = []
            for document in service.documents.all():
                document = DocumentSerializer(document)
                documentsList.append(document.data)
            dic = {
                "name": service.name,
                "branches": branchesForService,
                "documents": documentsList
            }
            agencyServices.append(dic)

        if(len(agencyServices) == 0):
            return JsonResponse("services list in agency is empty", safe=False)
        
        return JsonResponse(agencyServices, safe=False)
    return JsonResponse("wrong method type", safe=False)
    