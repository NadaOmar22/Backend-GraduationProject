from rest_framework import serializers
from .models import Service, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
    

class ServiceSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True)
    class Meta:
        model = Service
        fields = ('name', 'type', 'documents') 

