from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from ModelApp.serializers import ReviewSerializer
from ModelApp.MachineModel.sentimentanalysis_gpmodel import prediction

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        review = JSONParser().parse(request)        
        review_serializer = ReviewSerializer(data = review)
        if review_serializer.is_valid():
            review_serializer.save()
            sentiment = prediction(review['description'])
            return JsonResponse(sentiment, safe=False)
    else:
        return JsonResponse("Invalid Request Type", safe=False)


