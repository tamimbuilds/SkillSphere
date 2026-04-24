from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class CandidateProfile(models.Model):
    SECTOR_CHOICES = [
        ('android', 'Android App Development'),
        ('ios', 'iOS Development'),
        ('web_app', 'Web App'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('devops', 'DevOps'),
        ('fullstack', 'Fullstack'),
        ('ui_ux', 'UI/UX Design'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=100)
    specialized_sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, default='fullstack')
    university = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    cgpa = models.FloatField()
    graduation_year = models.IntegerField()
    bio = models.TextField(blank=True)
    resume_file = models.FileField(upload_to='resumes/')
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=200)
    recruiter_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_website = models.URLField(blank=True)
    company_address = models.TextField(blank=True)
    industry_type = models.CharField(max_length=100)
    company_size = models.IntegerField()

    def __str__(self):
        return f"{self.recruiter_name} — {self.company_name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
