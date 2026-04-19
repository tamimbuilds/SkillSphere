from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, CandidateProfileForm, RecruiterProfileForm
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
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def candidate_profile(request):
    if request.user.role != 'candidate':
        return redirect('home')
    profile = CandidateProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Profile saved.')
            return redirect('candidate_profile')
    else:
        form = CandidateProfileForm(instance=profile)
    return render(request, 'accounts/candidate_profile.html', {'form': form, 'profile': profile})


@login_required
def recruiter_profile(request):
    if request.user.role != 'recruiter':
        return redirect('home')
    profile = RecruiterProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = RecruiterProfileForm(request.POST, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Profile saved.')
            return redirect('recruiter_profile')
    else:
        form = RecruiterProfileForm(instance=profile)
    return render(request, 'accounts/recruiter_profile.html', {'form': form, 'profile': profile})


@login_required
def notifications(request):
    items = request.user.notifications.all()
    items.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {'notifications': items})
