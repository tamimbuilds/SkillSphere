from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, HiringInvitationForm, JobOfferForm, JobPostForm
from .models import Application, HiringInvitation, JobOffer, JobPost


def job_list(request):
    jobs = JobPost.objects.filter(status='open')
    applied_jobs = []
    if request.user.is_authenticated and request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        if candidate_profile is not None:
            applied_jobs = list(
                Application.objects.filter(candidate=candidate_profile).values_list('job_id', flat=True)
            )

    return render(request, 'job_list.html', {'jobs': jobs, 'applied_jobs': applied_jobs})


def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    has_applied = False
    if request.user.is_authenticated and request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        if candidate_profile is not None:
            has_applied = Application.objects.filter(candidate=candidate_profile, job=job).exists()

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
            messages.success(request, 'Job post created successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm()

    return render(request, 'job_form.html', {'form': form})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)

    if request.user.role != 'recruiter' or recruiter_profile != job.recruiter:
        messages.error(request, 'You are not allowed to edit this job post.')
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm(instance=job)

    return render(request, 'job_form.html', {'form': form, 'job': job})


@login_required
def dashboard(request):
    if request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        applications = Application.objects.filter(candidate=candidate_profile).select_related(
            'job', 'job__recruiter'
        )
        return render(request, 'dashboard.html', {'role': request.user.role, 'applications': applications})

    if request.user.role == 'recruiter':
        recruiter_profile = getattr(request.user, 'recruiter_profile', None)
        jobs = JobPost.objects.filter(recruiter=recruiter_profile).prefetch_related('application_set')
        return render(request, 'dashboard.html', {'role': request.user.role, 'jobs': jobs})

    return redirect('home')


@login_required
def my_applications(request):
    if request.user.role != 'candidate':
        return redirect('dashboard')

    candidate_profile = getattr(request.user, 'candidate_profile', None)
    applications = Application.objects.filter(candidate=candidate_profile).select_related('job', 'job__recruiter')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(JobPost, pk=pk, status='open')
    if request.user.role != 'candidate':
        return redirect('job_list')

    candidate_profile = getattr(request.user, 'candidate_profile', None)
    if candidate_profile is None:
        messages.error(request, 'Please complete your candidate profile before applying.')
        return redirect('profile')

    if Application.objects.filter(candidate=candidate_profile, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = candidate_profile
            app.job = job
            app.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form, 'job': job})
