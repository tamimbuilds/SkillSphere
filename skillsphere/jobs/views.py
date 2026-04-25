
from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, Application
from .forms import JobPostForm, ApplicationForm
from django.contrib.auth.decorators import login_required


def job_list(request):
    jobs = JobPost.objects.filter(status='open')
    applied_jobs = []
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'candidate':
        applied_jobs = Application.objects.filter(candidate=request.user.candidate_profile).values_list('job_id', flat=True)
    return render(request, 'job_list.html', {'jobs': jobs, 'applied_jobs': applied_jobs})


def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    has_applied = False
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'candidate':
        has_applied = Application.objects.filter(job=job, candidate=request.user.candidate_profile).exists()
    return render(request, 'job_detail.html', {'job': job, 'has_applied': has_applied})


@login_required
def job_create(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiter_profile
            job.save()
            return redirect('job_list')
    else:
        form = JobPostForm()

    return render(request, 'job_form.html', {'form': form})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(JobPost, pk=pk)

    if request.user.role != 'candidate':
        return redirect('job_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = request.user.candidate_profile
            app.job = job
            app.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form, 'job': job})


@login_required
def dashboard(request):
    if request.user.role == 'candidate':
        applications = Application.objects.filter(candidate=request.user.candidate_profile).select_related('job')
        return render(request, 'dashboard.html', {'applications': applications, 'role': 'candidate'})
    elif request.user.role == 'recruiter':
        jobs = JobPost.objects.filter(recruiter=request.user.recruiter_profile).prefetch_related('application_set')
        return render(request, 'dashboard.html', {'jobs': jobs, 'role': 'recruiter'})
    else:
        return redirect('job_list')