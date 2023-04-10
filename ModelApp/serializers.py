from rest_framework import serializers
from ModelApp.models import Review

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('ReviewId', 'Source', 'Destination', 'Description')      

