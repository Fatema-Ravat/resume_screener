from rest_framework import serializers
from .models import JobDescription,Resume
from .utils.resume_parser import  *

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ('id','parsed_text','parsed_at','matched_keywords','score','created_at')

    def create(self, validated_data):
        #save file
        resume_obj = super.create(validated_data)

        #parse file
        file_path = resume_obj.resume.path
        parse_text = None
        if ".docx" in file_path:
            parse_text = extract_text_from_doc(file_path)
        if ".pdf" in file_path:
            parse_text = extract_text_from_pdf(file_path)

        if parse_text is not None:
            resume_obj.parsed_text = parse_text
            if resume_obj.email is None or resume_obj.email == "":
                resume_obj.email = extract_email(parse_text)
            if resume_obj.phone is None or resume_obj.phone == "":
                resume_obj.phone = extract_phone(parse_text)
            if resume_obj.name is None or resume_obj.name == "":
                resume_obj.name = extract_name(parse_text)

            resume_obj.skills = extract_skills(parse_text)
    
            if resume_obj.experience_years is None:
                resume_obj.experience_years = extract_experience(parse_text)
            if resume_obj.education is None:
                resume_obj.education = extract_education(parse_text)

            resume_obj.save()
        else:
            print("Cannot parse the file")
        
        return resume_obj
        

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = "__all__"
        read_only_fields = ('id','created_at')