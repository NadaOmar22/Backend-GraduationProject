from django.views.decorators.csrf import csrf_exempt
from FacilityApp.models import Facility
from FacilityApp.serializers import DocumentSerializer
from AgencyApp.models import Branch
from AgencyApp.serializers import BranchSerializer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.hashers import make_password


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
    if request.method == 'POST':
        citizen_data = JSONParser().parse(request)
        if Citizen.objects.filter(email=citizen_data['email']):
            citizen = Citizen.objects.get(email=citizen_data['email'])
            password = citizen_data['password']
            print("encrupt")
            print(make_password(citizen_data['password']))
            if check_password(password, citizen.password):
                return JsonResponse("LoggedIn Successfully!!" , safe=False)
        return JsonResponse("Invalid email or password.", safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", safe=False)


@csrf_exempt
def CitizenEditProfileApi(request):
    if request.method=='POST':
        citizen_data=JSONParser().parse(request)
        CurrentCitizen = Citizen.objects.get(email=citizen_data['email'])
        CurrentCitizen.name = citizen_data['name']
        CurrentCitizen.email = citizen_data['email']
        CurrentCitizen.password = make_password(citizen_data['password'])
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
    branchName = branchSupervisor_data["branch"]
    branchObj = Branch.objects.get(name = branchName)
    if BranchSupervisor.objects.filter(govId=branchSupervisor_data["govId"]):
        return JsonResponse("Failed to Add.",safe=False)
    if BranchSupervisor.objects.filter(branch=branchObj):
        return JsonResponse("branch is already taken.",safe=False)
    branchSupervisor = BranchSupervisor(name=branchSupervisor_data["name"], password=branchSupervisor_data["password"], govId=branchSupervisor_data["govId"], branch=branchObj, supervisionType=branchSupervisor_data["supervisionType"], branchName=branchName)
    branchSupervisor.save()
    return JsonResponse("Added Successfully!!" , safe=False)

from django.contrib.auth.hashers import check_password

@csrf_exempt
def BranchSupervisorLoginApi(request):
    if request.method == 'POST':
        branchSupervisor_data = JSONParser().parse(request)
        if BranchSupervisor.objects.filter(govId = branchSupervisor_data['govId']):
            branchSupervisor = BranchSupervisor.objects.get(govId = branchSupervisor_data['govId'])
            password = branchSupervisor_data['password']
            if check_password(password, branchSupervisor.password):
                if branchSupervisor.isApproved == True:
                    return JsonResponse("LoggedIn Successfully!!" , safe=False)
                else:
                    return JsonResponse("Not Approved Yet!!" , safe=False)
            else:   
                return JsonResponse("Invalid Id or password.", safe=False)
    
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
            "branchLocation": requiredBranchSupervisior.branch.location,
            "supervisionType": requiredBranchSupervisior.supervisionType
        } 
        return JsonResponse(response,safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)
    
@csrf_exempt
def AgencySupervisorSignupApi(request):
    agencySupervisor_data = JSONParser().parse(request)
    agencyName = agencySupervisor_data["agency"]
    agencyObj = Agency.objects.get(name = agencyName)
    if AgencySupervisor.objects.filter(govId=agencySupervisor_data["govId"]):
        return JsonResponse("Failed to Add.",safe=False)
    if AgencySupervisor.objects.filter(agency=agencyObj):
        return JsonResponse("agency is already taken.",safe=False)
    agencySupervisor = AgencySupervisor(name=agencySupervisor_data["name"], password=agencySupervisor_data["password"], govId=agencySupervisor_data["govId"], agency=agencyObj, supervisionType=agencySupervisor_data["supervisionType"], agencyName=agencyName)
    agencySupervisor.save()
    return JsonResponse("Added Successfully!!" , safe=False)

@csrf_exempt
def AgencySupervisorLoginApi(request):
    if request.method == 'POST':
        agencySupervisor_data = JSONParser().parse(request)
        if AgencySupervisor.objects.filter(govId = agencySupervisor_data['govId']):
            agencySupervisor = AgencySupervisor.objects.get(govId = agencySupervisor_data['govId'])
            password = agencySupervisor_data['password']
            if check_password(password, agencySupervisor.password):
                if agencySupervisor.isApproved == True:
                    return JsonResponse("LoggedIn Successfully!!" , safe=False)
                else:
                    return JsonResponse("Not Approved Yet!!" , safe=False)
            else:   
                return JsonResponse("Invalid Id or password.", safe=False)
        return JsonResponse("Invalid Id or password.", safe=False)
    
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
        agency = Agency.objects.get(name = request_data['agencyName'])
        services = agency.allServices.all()
        branches = agency.branches.all()
        
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

@csrf_exempt
def BranchSupervisorEditProfileApi(request):
    if request.method=='POST':
        branch_data=JSONParser().parse(request)
        CurrentBranchSupervisor = BranchSupervisor.objects.get(govId=branch_data['govId'])
        CurrentBranchSupervisor.name = branch_data['name']
        CurrentBranchSupervisor.password = make_password(branch_data['password']) 
        CurrentBranchSupervisor.branch.location = branch_data['branchLocation']
        CurrentBranchSupervisor.branch.save()
        CurrentBranchSupervisor.save()
        return JsonResponse("Data updated Successfully!!" , safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)
    
@csrf_exempt
def AgencySupervisorEditProfile(request):
    if request.method=='POST':
        branch_data=JSONParser().parse(request)
        CurrentAgencySupervisor = AgencySupervisor.objects.get(govId=branch_data['govId'])
        CurrentAgencySupervisor.name = branch_data['name']
        CurrentAgencySupervisor.password = make_password(branch_data['password']) 
        CurrentAgencySupervisor.save()
        return JsonResponse("Data updated Successfully!!" , safe=False)
    else:
       return JsonResponse("Error: Wrong Method Type",safe=False)
