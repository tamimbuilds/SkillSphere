from django.urls import path
from . import views

urlpatterns = [
    # Candidate Skills (Main Interface)
    path('', views.candidate_skill_list, name='my_skills'),
    path('delete/<int:pk>/', views.delete_candidate_skill, name='delete_candidate_skill'),

    # Admin/General Skill List (moved to a different path if needed, or kept)
    path('all/', views.skill_list, name='skill_list'),
    path('all/add/', views.add_skill, name='add_skill'),

    # Certificate Management (Admin)
    path('admin-dashboard/', views.admin_certificate_dashboard, name='admin_certificate_dashboard'),
    path('verify/<int:pk>/', views.verify_certificate, name='verify_certificate'),
    path('reject/<int:pk>/', views.reject_certificate, name='reject_certificate'),

    # Certificate (Candidate)
    path('certificate/', views.certificate_list, name='certificate_list'),
    path('<int:pk>/certificate/add/', views.add_certificate, name='add_certificate'),
    path('certificate/<int:pk>/delete/', views.delete_certificate, name='delete_certificate'),
    path('view-certificate/<int:pk>/', views.view_certificate, name='view_certificate'),

    # Assessment
    path('assessment/', views.assessment_list, name='assessment'),
    path('<int:pk>/assessment/add/', views.add_assessment, name='add_assessment'),

    # Job Skill Requirement
    path('job-skills/', views.job_skill_requirement_list, name='job_skill_requirement_list'),
    path('job-skills/add/', views.add_job_skill_requirement, name='add_job_skill_requirement'),
]
