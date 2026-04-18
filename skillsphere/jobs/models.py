from django.db import models
from accounts.models import CandidateProfile, RecruiterProfile

class JobPost(models.Model):
    STATUS = [('open','Open'),('closed','Closed'),('draft','Draft')]
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_cgpa = models.FloatField()
    required_experience = models.IntegerField()
    salary_range = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    deadline = models.DateField()
    posted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='open')

    def __str__(self):
        return self.title

class HiringInvitation(models.Model):
    STATUS = [('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')]
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(null=True, blank=True)

class JobOffer(models.Model):
    STATUS = [('pending','Pending'),('accepted','Accepted'),('rejected','Rejected')]
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    offered_salary = models.FloatField()
    joining_date = models.DateField()
    offer_letter = models.FileField(upload_to='offers/')
    offer_status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Application(models.Model):
    STATUS = [
        ('applied','Applied'),
        ('shortlisted','Shortlisted'),
        ('rejected','Rejected'),
        ('offered','Offered'),
        ('hired','Hired'),
    ]
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidate', 'job')
