from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    path('recruiter/profile/', views.recruiter_profile, name='recruiter_profile'),
    path('candidate/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('notifications/', views.notifications, name='notifications'),
]
