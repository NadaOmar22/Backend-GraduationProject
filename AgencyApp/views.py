from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import BranchSerializer, AgencySerializer
from FacilityApp.models import Service
from rest_framework.parsers import JSONParser
from AgencyApp.models import Branch, Agency


@csrf_exempt   
def GetBranchesForAgencyAPI(request):
    if request.method == 'GET':
        agencyData = JSONParser().parse(request)
        agencyObj = Agency.objects.get(name = agencyData['name'])   
        branches = agencyObj.branches.all()
        serializer = BranchSerializer(branches, many=True)
        return JsonResponse (str(serializer.data), safe=False)
    else:
        return JsonResponse("Error: Wrong Method Type", status=400)
