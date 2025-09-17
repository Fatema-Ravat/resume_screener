from django.urls import path,include

from rest_framework import routers
from .views import ResumeViewSet,JobDescriptionViewSet

router = routers.DefaultRouter()
router.register(r'resumes',ResumeViewSet)
router.register(r'jobs',JobDescriptionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]