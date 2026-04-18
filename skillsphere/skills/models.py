from django.db import models
# from accounts.models import CandidateProfile
# from jobs.models import JobPost

# Create your models here.
class Skill(models.Model):
    skill_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.skill_name

class CandidateSkill(models.Model):
    # candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=50)
    years_of_experience = models.IntegerField()
    verified = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.candidate} - {self.skill}"

class Certificate(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected')
    ]

    candidate_skill = models.ForeignKey(CandidateSkill, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    certificate_file = models.FileField(upload_to='certificates/')
    issued_by = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    verification_status = models.CharField(max_length=20, choices=STATUS, default='pending')
    verified_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Assessment(models.Model):
    candidate_skill = models.ForeignKey(CandidateSkill, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=100)
    score = models.FloatField()
    passed = models.BooleanField(default=False)
    attempt_time = models.IntegerField()
    total_questions = models.IntegerField()
    attempt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate_skill} - {self.score}"

class JobSkillRequirement(models.Model):
    LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ]

    # job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='skill_requirements')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_level = models.CharField(max_length=20, choices=LEVEL)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        # unique_together = ('job', 'skill')
        pass

    # def __str__(self):
    #     return f"{self.job} - {self.skill}"