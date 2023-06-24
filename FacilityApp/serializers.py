from rest_framework import serializers
from .models import Service, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name',)

class ServiceSerializer(serializers.ModelSerializer):
    Documents = DocumentSerializer(many=True)

    class Meta:
        model = Service
        fields = ('name', 'type', 'documents') 