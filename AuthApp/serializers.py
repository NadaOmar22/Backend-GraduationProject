from rest_framework import serializers
from AuthApp.models import Citizen, BranchSupervisor, AgencySupervisor


class CitizenRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizen
        fields = ('UserId',
            'Name',
            'Email',
            'Password',
            'Gender',
            'PhoneNumber',
            'NationalId')
        
class BranchSupervisorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSupervisor
        fields = (
            'Name',
            'Email',
            'Password',
            'Gender',
            'GovId',
            'BranchName'
            )
class AgencySupervisorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgencySupervisor
        fields = (
            'Name',
            'Email',
            'Password',
            'Gender',
            'GovId',
            'AgencyName'
            )


