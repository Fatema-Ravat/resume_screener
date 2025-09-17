from rest_framework import serializers
from .models import JobDescription,Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"
        read_only_fields = ('id','parsed_text','parsed_at','matched_keywords','score','created_at')

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = "__all__"
        read_only_fields = ('id','created_at')