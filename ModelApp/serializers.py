from rest_framework import serializers
from ModelApp.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    destination = serializers.CharField(source = 'destination.name')
    relatedBranch = serializers.CharField(source = 'relatedBranch.name')
    class Meta:
        model = Review
        fields = ('reviewId', 'source', 'destination', 'relatedBranch', 'date', 'polarity', 'description', 'state')      

