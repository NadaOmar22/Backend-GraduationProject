from rest_framework import serializers
from .models import Branch, Agency
from FacilityApp.serializers import ServiceSerializer

class BranchSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    class Meta:
        model = Branch
        fields = ('name', 'services')

class AgencySerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True)
    class Meta:
        model = Agency
        fields = ('name', 'branches')