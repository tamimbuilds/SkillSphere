from django.urls import path
from . import views

urlpatterns = [
    path('', views.interview_list, name='interview_list'),
    path('schedule/', views.schedule_interview, name='schedule_interview'),
    path('shortlist/', views.shortlist_list, name='shortlist_list'),
    path('shortlist/add/', views.add_shortlist, name='add_shortlist'),
    path('interviewers/', views.interviewer_list, name='interviewer_list'),
    path('interviewers/add/', views.add_interviewer, name='add_interviewer'),
    path('<int:pk>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('<int:pk>/delete/', views.delete_interview, name='delete_interview'),
    path('<int:pk>/', views.interview_detail, name='interview_detail'),
]
