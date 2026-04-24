
from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, Application
from .forms import JobPostForm, ApplicationForm
from django.contrib.auth.decorators import login_required


def job_list(request):
    jobs = JobPost.objects.filter(status='open')
    return render(request, 'job_list.html', {'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    return render(request, 'job_detail.html', {'job': job})


@login_required
def job_create(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiterprofile
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
            app.candidate = request.user.candidateprofile
            app.job = job
            app.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form, 'job': job})