from rest_framework import serializers
from AuthApp.models import Citizen, BranchSupervisor, AgencySupervisor


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
    class Meta:
        model = BranchSupervisor
        fields = (
            'name',
            'password',
            'govId',
            'branchName'
            )
class AgencySupervisorSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencySupervisor
        fields = (
            'name',
            'password',
            'govId',
            'agencyName'
            )


