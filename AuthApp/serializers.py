from rest_framework import serializers
from AuthApp.models import Citizen, BranchSupervisor, AgencySupervisor
from AgencyApp.serializers import BranchSerializer



class CitizenSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ('userId',
            'name',
            'email',
            'password',
            'phoneNumber',
            'nationalId')
        
class BranchSupervisorSignupSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    class Meta:
        model = BranchSupervisor
        fields = (
            'name',
            'password',
            'govId',
            'branch',
            'supervisionType'
            )
class AgencySupervisorSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencySupervisor
        fields = (
            'name',
            'password',
            'govId',
            'agencyName',
            'supervisionType'
            )


