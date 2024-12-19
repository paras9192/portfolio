from rest_framework import serializers
from .models import Jobs
from apps.userProfile.models import UserData

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__' 

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__' 
