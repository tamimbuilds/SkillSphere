from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('applications/', views.my_applications, name='my_applications'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/edit/', views.job_edit, name='job_edit'),

    # Application URLs
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
]
