from django.contrib import admin
from jobs.models import JobPost, Application, HiringInvitation, JobOffer

admin.site.register(JobPost)
admin.site.register(Application)
admin.site.register(HiringInvitation)
admin.site.register(JobOffer)