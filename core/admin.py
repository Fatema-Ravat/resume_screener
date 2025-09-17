from django.contrib import admin
from .models import Resume,JobDescription

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','created_at','experience_years','score',)
    search_fields =('name','email','score','experience_years','skills',)
    list_filter = ('created_at',)

"""@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display =('id','title','required_skills','required_experience','created_at')
    search_fields('title','description')"""