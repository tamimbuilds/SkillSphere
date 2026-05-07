from django.urls import path

from jobs import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.my_applications, name='my_applications'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('applicants/<int:pk>/', views.job_applicants, name='job_applicants'),
    path('analysis/<int:pk>/', views.job_analysis, name='job_analysis'),
    path('offer/send/<int:application_pk>/', views.send_job_offer, name='send_job_offer'),
    path('offers/', views.offer_list, name='offer_list'),
    path('offer/<int:offer_pk>/respond/', views.respond_to_offer, name='respond_offer'),

    path('applications/<int:application_pk>/call-interview/', views.call_for_interview, name='call_for_interview'),

    # Job Skill Requirement management
    path('<int:pk>/skills/', views.job_skill_manage, name='job_skill_manage'),
    path('<int:pk>/skills/<int:skill_req_id>/delete/', views.job_skill_delete, name='job_skill_delete'),
]
