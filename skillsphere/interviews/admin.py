from django.contrib import admin
from .models import Interviewer, Shortlist, Interview

@admin.register(Interviewer)
class InterviewerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'designation', 'department', 'phone']
    list_filter = ['department', 'designation']
    search_fields = ['full_name', 'email', 'department']

@admin.register(Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'shortlisted_at', 'recruiter']
    list_filter = ['shortlisted_at', 'job']
    search_fields = ['candidate__user__first_name', 'candidate__user__last_name', 'job__title']

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'interviewer', 'interview_type', 'round_number', 'scheduled_date', 'status', 'score']
    list_filter = ['status', 'interview_type', 'scheduled_date']
    search_fields = ['candidate__user__first_name', 'candidate__user__last_name', 'interviewer__full_name']
    date_hierarchy = 'scheduled_date'