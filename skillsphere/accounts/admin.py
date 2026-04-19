from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CandidateProfile, RecruiterProfile, Notification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'phone', 'profile_image')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')


admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Notification)
