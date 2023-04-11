from rest_framework import serializers
from ModelApp.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('ReviewId', 'Source', 'Destination', 'Description', 'State')      

