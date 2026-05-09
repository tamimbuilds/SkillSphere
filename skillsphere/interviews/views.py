from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Interview, Interviewer, Shortlist
from .forms import InterviewForm, InterviewerForm, ShortlistForm
from django.contrib import messages

# Create your views here.

@login_required
def interviewer_list(request):
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can manage interviewers.")
        return redirect('dashboard')
    interviewers = Interviewer.objects.filter(recruiter=request.user.recruiter_profile).order_by('full_name')
    return render(request, 'interviewer_list.html', {'interviewers': interviewers})

@login_required
def add_interviewer(request):
    form = InterviewerForm(request.POST or None)
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can add interviewers.")
        return redirect('dashboard')
    if form.is_valid():
        interviewer = form.save(commit=False)
        interviewer.recruiter = request.user.recruiter_profile
        interviewer.save()
        messages.success(request, f'Interviewer "{interviewer.full_name}" added.')
        return redirect('interviewer_list')
    return render(request, 'interviewer_form.html', {'form': form})

@login_required
def delete_interviewer(request, pk):
    if request.user.role != 'recruiter':
        messages.error(request, "Only recruiters can remove interviewers.")
        return redirect('dashboard')

    interviewer = get_object_or_404(
        Interviewer,
        pk=pk,
        recruiter=request.user.recruiter_profile,
    )

    if request.method == 'POST':
        name = interviewer.full_name
        interviewer.delete()
        messages.success(request, f'Interviewer "{name}" removed.')

    return redirect('interviewer_list')

def shortlist_list(request):
    shortlists = Shortlist.objects.all()
    return render(request, 'shortlist.html', {'shortlists': shortlists})

def add_shortlist(request):
    form = ShortlistForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('shortlist_list')
    return render(request, 'shortlist_form.html', {'form': form})

@login_required
def interview_list(request):
    if request.user.role == 'candidate':
        interviews = Interview.objects.filter(candidate=request.user.candidate_profile).select_related('job', 'job__recruiter')
    elif request.user.role == 'recruiter':
        interviews = Interview.objects.filter(job__recruiter=request.user.recruiter_profile).select_related('candidate', 'job', 'job__recruiter')
    else:
        interviews = Interview.objects.none()
    return render(request, 'interview_list.html', {'interviews': interviews})


def schedule_interview(request):
    form = InterviewForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('interview_list')
    return render(request, 'schedule_interview.html', {'form': form})

@login_required
def submit_feedback(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    if request.method == 'POST':
        feedback = (request.POST.get('feedback') or '').strip()
        score_raw = (request.POST.get('score') or '').strip()

        if score_raw == '':
            score = None
        else:
            try:
                score = float(score_raw)
            except ValueError:
                messages.error(request, "Score must be a valid number between 0 and 10.")
                return render(
                    request,
                    'feedback_form.html',
                    {'interview': interview, 'submitted_feedback': feedback, 'submitted_score': score_raw},
                )

            if score < 0 or score > 10:
                messages.error(request, "Score must be between 0 and 10.")
                return render(
                    request,
                    'feedback_form.html',
                    {'interview': interview, 'submitted_feedback': feedback, 'submitted_score': score_raw},
                )

        interview.feedback = feedback
        interview.score = score
        interview.status = 'completed'
        interview.save()
        return redirect('interview_detail', pk=pk)
    return render(request, 'feedback_form.html', {'interview': interview})

@login_required
def interview_detail(request, pk):
    interview = get_object_or_404(
        Interview.objects.select_related('candidate', 'candidate__user', 'job', 'job__recruiter', 'interviewer'),
        pk=pk,
    )

    if request.user.role == 'candidate':
        if getattr(request.user, 'candidate_profile', None) != interview.candidate:
            messages.error(request, "You are not allowed to view this interview invitation.")
            return redirect('notifications')
    elif request.user.role == 'recruiter':
        if getattr(request.user, 'recruiter_profile', None) != interview.job.recruiter:
            messages.error(request, "You are not allowed to view this interview invitation.")
            return redirect('interview_list')
    else:
        messages.error(request, "You are not allowed to view this interview invitation.")
        return redirect('home')

    return render(request, 'interview_detail.html', {'interview': interview})

def delete_interview(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    interview.delete()
    return redirect('interview_list')
