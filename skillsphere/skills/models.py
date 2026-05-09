from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import CandidateProfile
from jobs.models import JobPost

# Create your models here.
class Skill(models.Model):
    SECTOR_CHOICES = [
        ('android', 'Android App Development'),
        ('ios', 'iOS Development'),
        ('web_app', 'Web App'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('devops', 'DevOps'),
        ('fullstack', 'Fullstack'),
        ('ui_ux', 'UI/UX Design'),
        ('mobile', 'Mobile Development'),
        ('data_science', 'Data Science'),
    ]
    skill_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=SECTOR_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.skill_name} ({self.get_category_display()})"


class Question(models.Model):
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    sector = models.CharField(max_length=100, choices=Skill.SECTOR_CHOICES)
    set_number = models.PositiveSmallIntegerField(default=1)
    question_order = models.PositiveSmallIntegerField(default=1)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sector', 'skill_id', 'set_number', 'question_order', 'id']
        unique_together = ('skill', 'set_number', 'question_order')

    def clean(self):
        super().clean()
        if self.skill_id:
            if self.skill.category != self.sector:
                raise ValidationError("Question sector must match the linked skill sector.")
            if not 1 <= self.set_number <= 3:
                raise ValidationError("Each skill can only have question sets 1 to 3.")
            if not 1 <= self.question_order <= 10:
                raise ValidationError("Each question set can only have question order 1 to 10.")

            existing = Question.objects.filter(skill=self.skill, set_number=self.set_number)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.count() >= 10:
                raise ValidationError("Each skill set can have a maximum of 10 questions.")

    def save(self, *args, **kwargs):
        if self.skill_id:
            self.sector = self.skill.category
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.skill_id:
            return f"{self.skill.skill_name} - Set {self.set_number} - Q{self.question_order}"
        return f"{self.get_sector_display()} - Q{self.pk or 'new'}"

class CandidateSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('1', '1 Year'),
        ('2', '2 Years'),
        ('3', '3 Years'),
        ('4', '4 Years'),
        ('5', '5 Years'),
        ('6', '6 Years'),
        ('7', '7 Years'),
        ('8', '8 Years'),
        ('9', '9 Years'),
        ('10', '10 Years'),
        ('10+', '10+ Years'),
    ]

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=50, choices=PROFICIENCY_CHOICES)
    years_of_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    verified = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['candidate', 'skill'], name='unique_candidate_skill')
        ]

    def clean(self):
        from django.core.exceptions import ValidationError
        try:
            if not self.pk and hasattr(self, 'candidate') and self.candidate: 
                if self.skill_id and CandidateSkill.objects.filter(candidate=self.candidate, skill_id=self.skill_id).exists():
                    raise ValidationError("You already added this skill. Remove it first if you want to add it again.")

                count = CandidateSkill.objects.filter(candidate=self.candidate).count()
                if count >= 3:
                    raise ValidationError("You can only add up to 3 specialized skills to prevent fraud.")
        except CandidateProfile.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.candidate} - {self.skill}"

    @property
    def verified_certificates_count(self):
        return self.certificate_set.filter(verification_status='verified').count()


class CandidateSkillProgress(models.Model):
    """
    Persistent assessment history for a candidate-skill pair.
    Keeps lock/penalty state even if CandidateSkill is removed and re-added.
    """
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='skill_progress_records')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='candidate_progress_records')
    add_count = models.PositiveSmallIntegerField(default=0)
    total_attempts = models.PositiveSmallIntegerField(default=0)
    total_failures = models.PositiveSmallIntegerField(default=0)
    current_cycle_attempts = models.PositiveSmallIntegerField(default=0)
    consecutive_failures = models.PositiveSmallIntegerField(default=0)
    times_blocked = models.PositiveSmallIntegerField(default=0)
    blocked_until = models.DateTimeField(null=True, blank=True)
    penalty_points = models.FloatField(default=0.0)
    last_attempt_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('candidate', 'skill')

    @property
    def is_blocked(self):
        return bool(self.blocked_until and self.blocked_until > timezone.now())

    def __str__(self):
        return f"{self.candidate} - {self.skill} progress"

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments')
    candidate_skill = models.ForeignKey(CandidateSkill, on_delete=models.CASCADE, related_name='assessments')
    score_record = models.ForeignKey('Score', on_delete=models.CASCADE, related_name='answers', null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='assessments')
    user_answer = models.CharField(max_length=1, choices=Question.OPTION_CHOICES)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('score_record', 'question')
        ordering = ['candidate_skill', 'question_id']

    def __str__(self):
        return f"{self.user} - {self.candidate_skill.skill.skill_name} - Q{self.question_id}"


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')
    candidate_skill = models.ForeignKey(CandidateSkill, on_delete=models.CASCADE, related_name='scores')
    attempt_number = models.PositiveSmallIntegerField(default=1)
    question_set_number = models.PositiveSmallIntegerField(default=1)
    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    score = models.FloatField(help_text='Percentage score')
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'candidate_skill', 'attempt_number')
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user} - {self.candidate_skill.skill.skill_name} - Attempt {self.attempt_number} - {self.score}%"

class JobSkillRequirement(models.Model):
    LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ]

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='skill_requirements')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    required_level = models.CharField(max_length=20, choices=LEVEL)
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        unique_together = ('job', 'skill')

    def __str__(self):
        return f"{self.job} - {self.skill}"
