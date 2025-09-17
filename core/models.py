from django.db import models

EDU_CHOICES=[
    ('none','None'),
    ('bachelor',"Bachelor's"),
    ('master',"Master's"),
    ('phd','PHD'),
]

class Resume(models.Model):
    # Resume Model

    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/')
    created_at = models.DateTimeField(auto_now_add=True)

    #parsed fields
    parsed_text = models.TextField(blank=True,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    experience_years = models.FloatField(blank=True,null=True)
    education = models.CharField(max_length=50,choices=EDU_CHOICES, blank=True,null=True)
    skills = models.JSONField(default=list,blank=True,null=True)
    score = models.FloatField(blank=True,null=True) #calculated
    matched_keywords = models.JSONField(default=dict,blank=True,null=True)
    parsed_at = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"Resume {self.id} : {self.name or 'unknown'}"
    

class JobDescription(models.Model):
    # Job descritption model

    title = models.CharField(max_length=250)
    decription = models.TextField()
    required_skills = models.JSONField(default=list,blank=True,help_text="List of required skills e.g.[Python, Java..]")
    required_experience = models.FloatField(blank=True,null=True,
                                                help_text="Years of experience required")
    required_education = models.CharField(choices=EDU_CHOICES,max_length=50,default="bachelor")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job: {self.title}"

