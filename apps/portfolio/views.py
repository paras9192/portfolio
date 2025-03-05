from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.userProfile.models import Jobs  
from apps.portfolio.models import PortFolio
from .models import ThemeMetaData
from apps.userProfile.models import UserData 
from apps.portfolio.serializer import ThemeMetaDataSerializer
from apps.portfolio.serializer import PortfolioSerializer
from rest_framework.viewsets import ModelViewSet
from chalkmate.utils import custom_success_response

class ThemeMetaDataViewSet(viewsets.ModelViewSet):
    queryset = ThemeMetaData.objects.all()
    serializer_class = ThemeMetaDataSerializer

    def create(self, request, *args, **kwargs):
        meta_data = request.data.get('meta_data', None)

        if not meta_data:
            return Response({"error": "meta_data is required"}, status=status.HTTP_400_BAD_REQUEST)
        job = Jobs.objects.create()
        mutable_data = request.data.copy()
        mutable_data['job_id'] = job.id

        serializer = self.get_serializer(data=mutable_data)
        if serializer.is_valid():
            theme_meta_data = serializer.save()
            return custom_success_response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PortFolioViewSet(ModelViewSet):
    queryset = PortFolio.objects.all()
    serializer_class = PortfolioSerializer
    
    def create(self, request, *args, **kwargs):
        job_id = request.data.get('job_id',None)
        job_data = Jobs.objects.filter(id=job_id).last()
        theme_data = ThemeMetaData.objects.filter(job_id=job_id).last()
        theme_meta_data = theme_data.meta_data
        
        if not theme_data:
            return Response({"error": "No Theme Meta Data found for the given job_id"}, status=status.HTTP_404_NOT_FOUND)
        user_data_obj = UserData.objects.filter(job_id=job_id).last()
        
        if not user_data_obj:
            return Response({"error": "No User Data found for the given job_id"}, status=status.HTTP_404_NOT_FOUND)
        user_data = user_data_obj.user_data
        if(user_data_obj.type=="YUCAMPUS"):
            final_json = create_final_json_yucampus(user_data,theme_meta_data)
        if(user_data_obj.type =="DIRECT"):
            final_json = create_final_json_direct(user_data, theme_meta_data)
        portfolio = PortFolio.objects.create(job_id=job_data, final_json=final_json)
        serializer = PortfolioSerializer(portfolio)
        return custom_success_response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        job_id = request.data.get('job_id', None)
        if not job_id:
            return Response({"error": "job_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        job_data = Jobs.objects.filter(id=job_id).last()
        if not job_data:
            return Response({"error": "Invalid job_id provided"}, status=status.HTTP_404_NOT_FOUND)
        
        theme_data = ThemeMetaData.objects.filter(job_id=job_id).last()
        if not theme_data:
            return Response({"error": "No Theme Meta Data found for the given job_id"}, status=status.HTTP_404_NOT_FOUND)
        
        user_data_obj = UserData.objects.filter(job_id=job_id).last()
        if not user_data_obj:
            return Response({"error": "No User Data found for the given job_id"}, status=status.HTTP_404_NOT_FOUND)
        
        theme_meta_data = theme_data.meta_data
        user_data = user_data_obj.user_data
        if user_data_obj.type =="YUCAMPUS":
            final_json = create_final_json_yucampus(user_data, theme_meta_data)
        if user_data_obj.type =="DIRECT":
            final_json = create_final_json_direct(user_data, theme_meta_data)
        
        instance.job_id = job_data
        instance.final_json = final_json
        instance.save()
        
        return custom_success_response(PortfolioSerializer(instance).data, status=status.HTTP_200_OK)
    


def create_final_json_yucampus(user_data,theme_data):
    name = user_data.get('name', '')
    # profile_pic = user_data.get('profile_pic', '')
    skills = [skill['title'] for skill in user_data.get('skills', [])]
    experience = user_data.get('experience', [])
    exp_count = len(experience)
    client_count = len(user_data.get('connections', []))
    resume = user_data.get('about', '')
    description = user_data.get('short_bio', '')
    landing_data = {
        "landing":{
        "user_name": name,
        "contact_me": user_data.get('user_email', ''),
        "explore_link": f"https://profile/{user_data.get('profile_link')}",
        "exp_count": exp_count,
        "client_count": client_count,
        "resume": resume,
        "skills": skills,
        "description":user_data.get("about",""),
        "designation":user_data.get("designation","")
        }
    }
    about_section = {
    "about": {
        "id": "about_me_1", 
        "about": user_data.get("about", ""), 
        "languages_known": [lang.strip() for lang in user_data.get("language_known", "").split(',') if lang.strip()], 
        "video_link": user_data.get("video_link", "")  
    }
    }
    
    experience_section = {
    "experience": {
        "description": "",
        "data": [
            {
                "company_name": exp.get("company", ""),  
                "job_title": exp.get("title", ""), 
                "job_description": exp.get("description", ""),
                "start_date": exp.get("start_date", ""),
                "end_date": exp.get("end_date", "") 
            }
            for exp in user_data.get("experience", {})  
        ]
    }
    }
    sevices_offered_section = {
        "sevices_offered":[]
        
    }
    
    education_section = {
        "education": {
            "description": "",
            "data": [
                {
                    
                    "univeristy": edu.get("school", ""),
                    "field": edu.get("field_of_study", ""),
                    "points": edu.get("description", ""),
                    "start_date": edu.get("start_date", ""), 
                    "end_date": edu.get("end_date", ""),
                }
                for edu in user_data.get("education", []) 
            ]
        }
    }
    skills_section = {
    "skills": [
        {
            "skill_name": skill.get("title", ""), 
            "skill_percentage": skill.get("skill_percentage", 0)  
        }
        for skill in user_data.get("skills", []) 
    ]
}
    license_section ={
        "license":[
            {
                "title": licence.get("name", ""), 
                "description": licence.get("description", ""),
                "organisation_logo": licence.get("upload_img", ""), 
                "organisation_name": licence.get("issuer", ""), 
                "issue_date": licence.get("issue_date", "") 
            }
            for licence in user_data.get("certification", []) 
        ]
    }
    portfolio_section ={
        "portfolio":[]
    }
    testimonial_section = {
        "testimonials": []
    }
    contact_data = user_data
    contact_me_section ={
        "contact_me":{
        "id": contact_data.get("id", ""),
        "name": contact_data.get("name", ""),
        "message": contact_data.get("about", ""),
        "phone": contact_data.get("phone", ""),
        "email": user_data.get("user_email", ""),
        "linkedin": contact_data.get("linkedin", ""),
        "facebook": contact_data.get("facebook", ""),
        "instagram": contact_data.get("instagram", ""),
        "medium": contact_data.get("medium", ""),
        "x": contact_data.get("x", ""),
    
        }
    }
    final_user_data={
        "data":{
        **landing_data,
        **about_section,
        **experience_section,
        **sevices_offered_section,
        **education_section,
        **skills_section,
        **license_section,
        **portfolio_section,
        **testimonial_section,
        **contact_me_section
        }
        
    }
    theme_data = {
        "theme":{
            **theme_data
        }
    }
    final_json_data = {
        **theme_data,
        **final_user_data
    }
    return final_json_data
    

def create_final_json_direct(user_data,theme_data):
    theme_data = {
        "theme":{
            **theme_data
        }
    }
    final_json_data = {
        **theme_data,
        **user_data
        
    }
    return final_json_data