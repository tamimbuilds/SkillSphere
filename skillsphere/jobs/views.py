from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import CandidateProfile, RecruiterProfile
from .models import JobPost, Application, HiringInvitation, JobOffer
from .forms import JobPostForm, ApplicationForm, HiringInvitationForm, JobOfferForm


# ─── Job List ─────────────────────────────────────────────────
def job_list(request):
    jobs = JobPost.objects.filter(status='open')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ─── Job Detail ───────────────────────────────────────────────
def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    has_applied = False

    if request.user.is_authenticated and request.user.role == 'candidate':
        has_applied = Application.objects.filter(
            candidate=request.user.candidate_profile,
            job=job,
        ).exists()

    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})


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

    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def dashboard(request):
    context = {'role': request.user.role}

    if request.user.role == 'candidate':
        context['applications'] = Application.objects.filter(
            candidate=request.user.candidate_profile
        ).select_related('job', 'job__recruiter')
    elif request.user.role == 'recruiter':
        context['jobs'] = JobPost.objects.filter(
            recruiter=request.user.recruiter_profile
        )

    return render(request, 'dashboard.html', context)


@login_required
def job_edit(request, pk):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    job = get_object_or_404(JobPost, pk=pk, recruiter=request.user.recruiter_profile)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job post updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'job': job})


# ─── Apply to Job (Candidate only) ───────────────────────────
@login_required
def apply_job(request, pk):
    job = get_object_or_404(JobPost, pk=pk, status='open')
    if request.user.role != 'candidate':
        return redirect('job_list')
    if Application.objects.filter(candidate=request.user.candidate_profile, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = request.user.candidate_profile
            app.job = job
            app.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply.html', {'form': form, 'job': job})
