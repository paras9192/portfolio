from apps.portfolio.models import PortFolio
from apps.userProfile.models import Jobs
from .models import ThemeMetaData
from rest_framework import serializers

class ThemeMetaDataSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(queryset=Jobs.objects.all(), required=False)
    class Meta:
        model = ThemeMetaData
        fields = '__all__'
        
class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortFolio
        fields = '__all__'
   