from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Interview, Interviewer, Shortlist

# Create your views here.

def interview_list(request):
    return render(request, 'interviews/interview_list.html')

def schedule_interview(request):
    return render(request, 'interviews/schedule_interview.html')

def interview_detail(request, pk):
    return render(request, 'interviews/interview_detail.html')

def submit_feedback(request, pk):
    return render(request, 'interviews/feedback_form.html')

def shortlist_list(request):
    return render(request, 'interviews/shortlist.html')

def add_shortlist(request):
    return redirect('shortlist_list')

def interviewer_list(request):
    return render(request, "interview_list.html")
