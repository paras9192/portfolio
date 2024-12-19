from rest_framework.viewsets import ModelViewSet

from chalkmate.utils import custom_success_response, get_yucampus_profile
from .models import Jobs 
from apps.userProfile.models import UserData
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .serializer import JobsSerializer
from apps.userProfile.serializer import UserDataSerializer
import json
from PyPDF2 import PdfReader

class JobsViewSet(ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer
    
class UserDataViewSet(ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    
    def create(self, request, *args, **kwargs):
        data_type = request.data.get('type')

        if data_type == "YUCAMPUS":
            profile_id = request.data.get('profile_id')
            if not profile_id:
                raise ValidationError({'message': ['No profile_id provided']})
            user_data = get_yucampus_profile(profile_id)
            if not user_data:
                raise ValidationError({'message': ['Failed to fetch YUCAMPUS profile data']})
            json_data = {
                'type': data_type,
                'profile_id': profile_id,
                'user_data': user_data['data'],
                'job_id': request.data.get('job_id'),
            }

            serializer = UserDataSerializer(data=json_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return custom_success_response(serializer.data, status=status.HTTP_201_CREATED)
        # if data_type == "DIRECT":
        #     if 'resume' in request.FILES:
        #         resume_file = request.FILES['resume']

        #     # Read and extract text from the PDF
        #         pdf_reader = PdfReader(resume_file)
        #         pdf_text = ""
        #         for page in pdf_reader.pages:
        #             pdf_text += page.extract_text()
        #         json_data = {}
        #         for line in pdf_text.split("\n"):
        #              if ":" in line:  
        #                 key, value = map(str.strip, line.split(":", 1))
        #                 json_data[key] = value

            
        #     print("Extracted PDF Text:", json_data)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return custom_success_response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data_type = request.data.get('data_type')

        if data_type == "YUCAMPUS":
            profile_id = request.data.get('profile_id')
            if not profile_id:
                raise ValidationError({'message': ['No profile_id provided']})
        
            user_data = get_yucampus_profile(profile_id)
            if not user_data:
                raise ValidationError({'message': ['Failed to fetch YUCAMPUS profile data']})

            instance.user_data = user_data['data']
            instance.profile_id = profile_id
            instance.save()

            serializer = self.get_serializer(instance)
            return custom_success_response(serializer.data, status=status.HTTP_200_OK)
    
        if data_type == "DIRECT":
            
            user_data = request.data['user_data']
            user_data = json.loads(user_data)
            instance.user_data = user_data  
            instance.save()

            serializer = self.get_serializer(instance)
            return custom_success_response(serializer.data, status=status.HTTP_200_OK)
    
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_success_response(serializer.data, status=status.HTTP_200_OK)
