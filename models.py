from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    skills = models.TextField()
    experience = models.FloatField(default=0)  # Set a default value
    education = models.TextField()
    resume_file = models.FileField(upload_to='resumes/')

    def __str__(self):
        return self.name
