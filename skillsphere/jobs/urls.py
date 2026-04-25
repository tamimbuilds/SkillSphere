from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
]