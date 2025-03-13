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
import re
import random
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
        elif data_type == "DIRECT":
            user_data = request.data['user_data']
            try:
                user_data = request.data['user_data']
                parsed_user_data = json.loads(user_data)
            except (KeyError, json.JSONDecodeError) as e:
                raise ValidationError({"user_data": "Invalid JSON format"})
            json_data = {
                'type': data_type,
                'user_data': parsed_user_data,
                'job_id': request.data.get('job_id'),
            }
            serializer = self.get_serializer(data=json_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return custom_success_response(serializer.data, status=status.HTTP_201_CREATED)
        elif data_type == "RESUME":
            if 'resume' in request.FILES:
                resume_file = request.FILES['resume']
                pdf_reader = PdfReader(resume_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()
                data = transform_pdf_text_to_json(pdf_text)
                json_data = {
                'type': data_type,
                'user_data': data,
                'job_id': request.data.get('job_id'),
            }
                serializer = self.get_serializer(data=json_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                return custom_success_response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError({'message': ['No resume file provided']})
            
            
    
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
    
        elif data_type == "DIRECT":
            
            user_data = request.data['user_data']
            user_data = json.loads(user_data)
            instance.user_data = user_data  
            instance.save()

            serializer = self.get_serializer(instance)
            return custom_success_response(serializer.data, status=status.HTTP_200_OK)
        elif data_type == "RESUME":
            if 'resume' not in request.FILES:
                raise ValidationError({'message': ['No resume file provided']})

            resume_file = request.FILES['resume']
            try:
                pdf_reader = PdfReader(resume_file)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extract_text()
                data = transform_pdf_text_to_json(pdf_text)
            except Exception as e:
                raise ValidationError({'message': [f'Error processing resume: {str(e)}']})

            instance.user_data = data
            instance.save()

            serializer = self.get_serializer(instance)
            return custom_success_response(serializer.data, status=status.HTTP_200_OK)

        else:
            raise ValidationError({'message': ['Invalid data_type provided']})
            
    
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return custom_success_response(serializer.data, status=status.HTTP_200_OK)



def transform_pdf_text_to_json(pdf_text):
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    
    headings = {
        "user_name": ["User Name", "Full Name", "Name"],
        "phone": ["Phone", "Phone Number", "Contact Number"],
        "email": ["Email", "Email Address"],
        "linkedin": ["LinkedIn", "LinkedIn Profile"],
        "explore_link": ["Explore Link", "Website", "Portfolio Link"],
        "skills": ["Skills", "Expertise", "Core Competencies"],
        "languages": ["Languages", "Languages Known"],
        "description": ["About", "Description", "Summary"],
        "internship": ["Internship"],
        "projects": ["Portfolio", "Projects", "Work Samples"],
        "education":["education"],
        'sevices_offered':['sevices_offered']
    }


    data = {
        "user_data": {
            "landing": {
                "user_name": "",
                "contact_me": "",
                "explore_link": "",
                "exp_count": 0,
                "client_count": 0,
                "resume": "",
                "skills": [],
                "description": "",
                "designation":""
            },
            "about": {
                "id": "about_me_1",
                "about": "",
                "languages_known": [],
                "video_link": ""
            },
            "experience": {
                "description": "",
                "data": []
            },
            "education": {
                "description": "",
                "data": []
            },
            "sevices_offered":[],
            "skills": [],
            "license": [],
            "portfolio": [],
            "testimonials": [],
            "contact_me": {
                "id": 313,
                "name": "",
                "message": "",
                "phone": "",
                "email": "",
                "linkedin": "",
                "facebook": "",
                "instagram": "",
                "medium": "",
                "x": ""
            }
        }
    }
    
    
    def match_heading(text, heading_dict):
        highest_score = 0
        best_match = None
        matched_phrase = None

        for key, phrases in heading_dict.items():  
            for phrase in phrases: 
                words = phrase.split() 
                for word in words:
                    match, score = process.extractOne(text, [word], scorer=fuzz.partial_ratio) 
                    
                    if score > highest_score:
                        highest_score = score
                        best_match = key  
                        matched_phrase = match 

        if highest_score >= 80:  
            return best_match
        return None  

    

    if pdf_text:
        lines = pdf_text.split("\n")

        for i, line in enumerate(lines):
            matched_heading = match_heading(line, headings)
            if matched_heading:
                if matched_heading == "skills":
                    skills_text = lines[i + 1] if i + 1 < len(lines) else ""
                    raw_skills = re.split(r"[,.\s]+", skills_text)
                    filtered_skills = [skill for skill in raw_skills if len(skill) > 1]
                    skill_objects = [
                    {"skill_name": skill, "skill_percentage": random.randint(1, 100)}
                    for skill in set(filtered_skills)
                     ]
                    data["user_data"]["landing"]["skills"] =filtered_skills
                    data["user_data"]["skills"] = skill_objects

                elif matched_heading == "languages":
                    languages_text = lines[i + 1] if i + 1 < len(lines) else ""
                    raw_languages = re.split(r"[,.\s]+", languages_text)
                    filtered_languages = [lang for lang in raw_languages if len(lang) > 1]
                    data["user_data"]["about"]["languages_known"] = list(set(filtered_languages))
        
                if matched_heading == "internship":
                    internship_entries = []
                    for j in range(i + 1, len(lines)):
                        current_line = lines[j].strip()
                        if re.match(r".+\sMM YYYY – MM YYYY", current_line):
                            
                            company_role = current_line.split(" MM YYYY – MM YYYY")
                            company_name = company_role[0].strip() if len(company_role) > 0 else ""
                            role = company_role[1].strip() if len(company_role) > 1 else ""
                            internship_entries.append({
                            "start_date": "MM YYYY", 
                            "end_date": "MM YYYY",    
                            "company_name": company_name,
                            "job_title": role,
                            "description": ""
                            })
                        if "experience" not in data["user_data"]:
                            data["user_data"]["experience"] = {"description": "", "data": []}
                        if "data" not in data["user_data"]["experience"]:
                            data["user_data"]["experience"]["data"] = []
                        
                    data["user_data"]["experience"]["data"].extend(internship_entries)
                
                if matched_heading == "services_offered":
                    services_text = lines[i + 1] if i + 1 < len(lines) else ""
                    raw_services = re.split(r"[,\n]+", services_text)
                    filtered_services = [service.strip() for service in raw_services if service.strip()]
                    data["user_data"]["services_offered"] = list(set(filtered_services))
                
                if matched_heading == "education":
                    internship_entries = []
                    for j in range(i + 1, len(lines)):
                        current_line = lines[j].strip()
                        if re.match(r".+\sMM YYYY – MM YYYY", current_line):
                            
                            company_role = current_line.split(" MM YYYY – MM YYYY")
                            company_name = company_role[0].strip() if len(company_role) > 0 else ""
                            degree = company_role[1].strip() if len(company_role) > 1 else ""
                            internship_entries.append({
                            "start_date": "MM YYYY",  
                            "end_date": "MM YYYY",   
                            "university": company_name,
                            "field": degree,
                            "description": ""
                            })
                        if "education" not in data["user_data"]:
                            data["user_data"]["education"] = {"description": "", "data": []}
                        if "data" not in data["user_data"]["education"]:
                            data["user_data"]["education"]["data"] = []
                        
                    data["user_data"]["education"]["data"].extend(internship_entries)

                elif matched_heading == "description":
                    description_lines = []
                    for j in range(i + 1, len(lines)):
                        if match_heading(lines[j].strip(), headings):
                            break
                        description_lines.append(lines[j].strip())
                    data["user_data"]["landing"]["description"] = " ".join(description_lines).strip()

                elif matched_heading == "projects":
                    project_pattern = re.compile(r"(.*?)\|(.*?)MM YYYY")
                    description_pattern = re.compile(r"•(.*?)\n")
                    projects = []
                    project_matches = project_pattern.findall(pdf_text)
                    if project_matches:
                        for match in project_matches:
                            project_name = match[0].strip()
                            tech_stack = match[1].strip()
                            descriptions = description_pattern.findall(pdf_text)
                            projects.append({
                            "project_name": project_name,
                            "tech_stack": tech_stack,
                            "date": "MM YYYY", 
                            "description": " ".join([desc.strip() for desc in descriptions])
                                                })         
                    data["user_data"]["portfolio"] = projects


        phone_match = re.search(r"\+?\d{1,4}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}", pdf_text)
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", pdf_text)
        linkedin_match = re.search(r"https?://(www\.)?linkedin\.com/[^\s]+", pdf_text)
        name_match=re.search(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", pdf_text)
        data["user_data"]["contact_me"]["phone"] = phone_match.group(0) if phone_match else ""
        data["user_data"]["contact_me"]["email"] = email_match.group(0) if email_match else ""
        data["user_data"]["contact_me"]["linkedin"] = linkedin_match.group(0) if linkedin_match else ""
        data["user_data"]["contact_me"]["name"] =name_match.group(0) if name_match else ""
        data["user_data"]["landing"]["user_name"]=name_match.group(0) if name_match else ""
        data["user_data"]["landing"]["contact_me"]=phone_match.group(0) if phone_match else ""

    

    return data
