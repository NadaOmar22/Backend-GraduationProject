from ModelApp.models import Review
from FacilityApp.models import Facility, Document
from http.client import HTTPResponse
from django.http import Http404 , FileResponse
import os
from FacilityApp.models import  App, Service
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import ServiceSerializer, DocumentSerializer
from AgencyApp.models import Branch,Agency
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import requests
from bs4 import BeautifulSoup
import csv


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
    if request.method == 'POST':
        requestData = JSONParser().parse(request)
        serviceObj = Service.objects.get(name = requestData['serviceName'])   
        documents = serviceObj.documents.all()
        doucmentsNamesList = []
        for document in documents:
            doucmentsNamesList.append(document.name)
        response = {
            "documents" : doucmentsNamesList
        }
        return JsonResponse (response, safe=False)
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
def AddServiceForAgencyAPI(request):
    if request.method == 'POST':
        serviceData = JSONParser().parse(request)
        
        agency = Agency(name=serviceData['agencyName'])
        agency_exists = Agency.objects.filter(name=agency.name).exists()
        if agency_exists:
            agency = Agency.objects.get(name=agency.name)
        else:
            return JsonResponse("Error: Agency Name Does't Exsit" , safe=False)
            #agency.save()

        service = Service(name=serviceData['serviceName'])
        service_exists = Service.objects.filter(name=service.name).exists()
        if service_exists:
            print(service_exists)
            return JsonResponse("Error: Service Name Already Exit" , safe=False)
            #service = Service.objects.get(name=service.name)
        else:
            service.save()

        serviceDocuments = []
        for document_data in serviceData['documents']:
            document = Document(name=document_data['documentName'])
            document_exists = Document.objects.filter(name=document.name).exists()
            if document_exists:
                document = Document.objects.get(name=document.name)
            else:
                document.save()
                serviceDocuments.append(document)
        service.documents.set(serviceDocuments)
        service.save()
        agency.allServices.add(service)
        agency.save()

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
            if review.relatedBranch.services.all().filter(name=review.destination.name).exists():
                dict = {
                        "description":review.description,
                        "serviceName":review.destination.name,
                        "state": review.state,
                        'date': review.date,
                        'reviewId' : review.reviewId
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

         
# Web Scraping
# Magic         
@csrf_exempt
def ScrapDocumentApi(request):
    serviceNames = []
    serviceDocuments = []

    page = requests.get("https://psm.gov.eg/providers/1/services")

    src = page.content
    soup = BeautifulSoup(src, "html.parser")

    services = soup.find_all("div", {"class" : "media-body text-right pr-4"})

    for i in range(len(services)):
        serviceNames.append(services[i].contents[1].text.strip())

        try:
            serviceObj = Service.objects.get(name=serviceNames[i])
        except Service.DoesNotExist:
            serviceObj = Service(name=serviceNames[i])
            serviceObj.save() 
        servicePage = requests.get(f"https://psm.gov.eg{services[i].contents[1]['href']}&district_id=2&governorate_id=1&districtName=حي-الزاوية-الحمراء&governorateName=القاهرة")
        servicePageSrc =  servicePage.content  
        soup2 = BeautifulSoup(servicePageSrc, "html.parser")  
        serviceDocumentsList = soup2.find("ol").find_all("li")
        serviceDocumentsList2 = []
        [serviceDocumentsList2.append(x.text.strip()) for x in serviceDocumentsList]

        for document in serviceDocumentsList2:
            if document[0].isdigit():
                document = document.split(' ', 1)[1]
            try:
                documentObj = Document.objects.get(name=document)
            except Document.DoesNotExist:
                documentObj = Document(name=document)
                documentObj.save()
            serviceObj.documents.add(documentObj)
        serviceObj.save()

    response = {
        'serviceName' : serviceNames,
        'serviceDocuments' : serviceDocuments,
    }

    return JsonResponse(response,safe=False)


@csrf_exempt
def GetAllServicesApi(request):
    services = Service.objects.all()
    response = []
    for service in services:
        data = ServiceSerializer(service)
        response.append(data.data)
    return JsonResponse(response, safe = False)

@csrf_exempt
def GetAllDocumentsApi(request):
    documents = Document.objects.all()
    response = []
    for document in documents:
        response.append(document.name)
    return JsonResponse(response, safe = False)   

@csrf_exempt
def UpdateServiceApi(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        serviceObj = Service.objects.get(name = request_data['name'])
    
        serviceDocuments = []
        for document_data in request_data['documents']:
            document_exists = Document.objects.filter(name=document_data['name']).exists()
            if document_exists:
                document = Document.objects.get(name=document_data['name'])
            else:
                document = Document(name=document_data['name'])
                document.save()
            serviceDocuments.append(document)
        
        serviceObj.documents.set(serviceDocuments)
        serviceObj.save()
            
        return JsonResponse("Updates Saved!!", safe = False)
    return JsonResponse("Wrong Method Type!!", safe = False)
    
       
