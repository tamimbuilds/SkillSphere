from django.urls import path

from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.my_applications, name='my_applications'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/applicants/', views.job_applicants, name='job_applicants'),
    path('<int:pk>/analysis/', views.job_analysis, name='job_analysis'),

    # Job Skill Requirement management
    path('<int:pk>/skills/', views.job_skill_manage, name='job_skill_manage'),
    path('<int:pk>/skills/<int:skill_req_id>/delete/', views.job_skill_delete, name='job_skill_delete'),
]

