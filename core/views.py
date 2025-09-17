from django.shortcuts import render

from rest_framework import viewsets
from .models import Resume,JobDescription
from .serializers import ResumeSerializer,JobDescriptionSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all().order_by('-created_at')
    serializer_class = ResumeSerializer

class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all().order_by("-created_at")
    serializer_class = JobDescriptionSerializer