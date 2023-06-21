from ModelApp.models import Review
from FacilityApp.models import Facility
from http.client import HTTPResponse
from django.http import Http404 , FileResponse
import os
from FacilityApp.models import  App, Service
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import ServiceSerializer, DocumentSerializer
from AgencyApp.models import Branch
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site



@csrf_exempt
def GetFacilityReviewsApi(request):
    if request.method == 'GET':
        facility_data=JSONParser().parse(request)
        facility = Facility.objects.get(name = facility_data['name'])
        return JsonResponse (str(Review.objects.filter(destination = facility).values()), safe=False)
    else:
       return JsonResponse ("Error: Wrong Method Type",safe=False)  


@csrf_exempt   
def ServeImage(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    #print("i will show you youmna!", file_path)
    if os.path.exists(file_path):
        image = open(file_path, 'rb')  #rb : binary format
        response = FileResponse(image)
        print(response)
        return response
    raise Http404


def get_current_host(request):
    current_site = get_current_site(request)
    return current_site.domain


@csrf_exempt   
def GetAppsAPI(request):
    if request.method == 'GET':
        apps = list(App.objects.all().values())
        localHost = get_current_host(request)
        imageURL = "http://"+localHost+'/'+settings.MEDIA_ROOT
        for i in range(len(apps)):
            imageName = App.objects.get(name = apps[i]['name']).cover.name
            apps[i]['cover'] = imageURL+imageName+'/'    
        return JsonResponse(apps, safe=False)


@csrf_exempt   
def GetServicesForBranchAPI(request):
    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        branchObj = Branch.objects.get(name = requestData['branchName'])   
        services = branchObj.services.all()
        print(services)
        response = []
        for service in services:
            response.append(service.name)
        return JsonResponse (response, safe=False)
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
        serviceObj = Service.objects.get(name = requestData['name'])   
        documents = serviceObj.Documents.all()
        serializer = DocumentSerializer(documents, many=True)
        return JsonResponse (str(serializer.data), safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)
    
@csrf_exempt   
def AddDocumentAPI(request):
    if request.method == 'POST':
        documentData = JSONParser().parse(request)
        documentSerializer = DocumentSerializer(data = documentData)
        if documentSerializer.is_valid():
            documentSerializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
@csrf_exempt   
def AddServiceAPI(request):
    if request.method == 'POST':
        serviceData = JSONParser().parse(request)
        print(serviceData)
        serviceSerializer = ServiceSerializer(data = serviceData)
        print(serviceSerializer)
        if serviceSerializer.is_valid():
            serviceSerializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    

@csrf_exempt
def ServiceReviewsFilteredByYearApi(request):
    if request.method == 'POST':
        print(request)
        request_data = JSONParser().parse(request)
        facilityObj = Facility.objects.get(name = request_data['serviceName'])
        branchObj = Branch.objects.get(name = request_data['branchName'])

        year = request_data['year']
        
        reviews = Review.objects.filter(destination = facilityObj, 
                                        relatedBranch = branchObj,
                                        date__year = year
                                        )

        positiveList = []
        negativeList = []
        neutralList = []

        for review in reviews:
            dict = {
                    "description":review.description,
                    "state": review.state,
                    "serviceName" : request_data['serviceName'],
                    "date" : review.date
                }
            if review.polarity == "positive":  
                positiveList.append(dict)
            elif review.polarity == "negative":
                negativeList.append(dict)
            elif review.polarity == "neutral":
                neutralList.append(dict)
         
        response_data = {
            'positiveList': positiveList,
            'negativeList': negativeList,
            'neutralList': neutralList
        }

        return JsonResponse(response_data, safe=False)
    
    return JsonResponse("Invalid.",safe=False)  

@csrf_exempt
def BranchReviewsFilteredByYearApi(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        branchObj = Branch.objects.get(name = request_data['branchName'])

        year = request_data['year']

        reviews = Review.objects.filter(relatedBranch = branchObj, date__year = year)

        positiveList = []
        negativeList = []
        neutralList = []

        for review in reviews:
            dict = {
                    "description":review.description,
                    "serviceName":review.destination.name,
                    "state": review.state,
                    'date': review.date,
                }
            if review.polarity == "positive":  
                positiveList.append(dict)
            elif review.polarity == "negative":
                negativeList.append(dict)
            elif review.polarity == "neutral":
                neutralList.append(dict)
         
        response_data = {
            'positiveList': positiveList,
            'negativeList': negativeList,
            'neutralList': neutralList
        }
        
        return JsonResponse(response_data, safe=False)
    return JsonResponse("Invalid.",safe=False)  
 

@csrf_exempt
def ReviewsYearsFilteredByBranchApi(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        branchObj = Branch.objects.get(name = request_data['branchName'])

        reviews = Review.objects.filter(relatedBranch = branchObj)

        reviewsYear = set()
        for review in reviews:
            reviewsYear.add(review.date.year)
        response = list(reviewsYear)
        return JsonResponse(response, safe=False)
    return JsonResponse("Invalid.",safe=False)  

         


