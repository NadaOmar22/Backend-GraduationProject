from django.shortcuts import render
from .models import Administrator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

@csrf_exempt
def AdministratorLoginApi(request):
    if request.method == 'POST':
        administrator_data = JSONParser().parse(request)
        obj = Administrator.load()
        if obj.username == administrator_data['username'] and obj.password  == administrator_data['password']:
            return JsonResponse("LoggedIn Successfully!!", safe=False)
        return JsonResponse("Invalid username or password.",safe=False)
