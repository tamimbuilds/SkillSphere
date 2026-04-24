from django.contrib import admin
from .models import Interview, Interviewer, Shortlist

# Register your models here.

@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'designation']


@admin.register(Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'shortlisted_at']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'interview_type', 'status', 'score']