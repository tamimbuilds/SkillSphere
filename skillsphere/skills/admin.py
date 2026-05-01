from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Skill, Question, CandidateSkill, Certificate, Assessment, Score, JobSkillRequirement

admin.site.register(Skill)
admin.site.register(Question)
admin.site.register(CandidateSkill)
admin.site.register(Certificate)
admin.site.register(Assessment)
admin.site.register(Score)
admin.site.register(JobSkillRequirement)
