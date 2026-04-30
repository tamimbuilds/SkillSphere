from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, CandidateProfileForm, RecruiterProfileForm, UserUpdateForm
from .models import CandidateProfile, RecruiterProfile, Notification


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'candidate':
                return redirect('candidate_profile')
            return redirect('recruiter_profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    user = request.user
    user_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)
    
    if user.role == 'candidate':
        profile, created = CandidateProfile.objects.get_or_create(
            user=user,
            defaults={'full_name': user.get_full_name() or user.username, 'cgpa': 0.0, 'graduation_year': 2024}
        )
        profile_form = CandidateProfileForm(request.POST or None, request.FILES or None, instance=profile)
    else:
        profile, created = RecruiterProfile.objects.get_or_create(
            user=user,
            defaults={'recruiter_name': user.get_full_name() or user.username, 'company_name': 'Pending', 'company_size': 1}
        )
        profile_form = RecruiterProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    # Fetch skills if candidate
    skills = []
    total_jobs = 0
    total_interviews = 0
    
    from jobs.models import Application, JobPost
    from interviews.models import Interview

    if user.role == 'candidate':
        from skills.models import CandidateSkill, Score
        skills = CandidateSkill.objects.filter(candidate=profile).select_related('skill')
        for s in skills:
            score_qs = Score.objects.filter(user=user, candidate_skill=s).order_by('-attempt_number', '-completed_at')
            s.latest_score = score_qs.first()
            s.attempt_count = score_qs.count()
            s.has_assessment = s.latest_score is not None
        total_jobs = Application.objects.filter(candidate=profile).count()
        total_interviews = Interview.objects.filter(candidate=profile).count()
    elif user.role == 'recruiter':
        total_jobs = JobPost.objects.filter(recruiter=profile).count()
        total_interviews = Interview.objects.filter(job__recruiter=profile).count()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'role': user.role,
        'skills': skills,
        'total_jobs': total_jobs,
        'total_interviews': total_interviews,
    }
    return render(request, 'profile.html', context)


@login_required
def candidate_profile(request):
    return redirect('profile')


@login_required
def recruiter_profile(request):
    return redirect('profile')


@login_required
def notifications(request):
    items = request.user.notifications.all()
    items.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications.html', {'notifications': items})
