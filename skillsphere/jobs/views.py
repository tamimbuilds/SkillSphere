from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, HiringInvitationForm, JobOfferForm, JobPostForm
from .models import Application, HiringInvitation, JobOffer, JobPost
from .utils import calculate_match_score
from skills.models import Skill, JobSkillRequirement


def job_list(request):
    jobs = JobPost.objects.filter(status='open').select_related('recruiter')
    candidate_profile = None
    
    if request.user.is_authenticated and request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        if candidate_profile:
            applied_job_ids = set(Application.objects.filter(candidate=candidate_profile).values_list('job_id', flat=True))
            for job in jobs:
                job.match_score = calculate_match_score(candidate_profile, job)
                job.has_applied = job.id in applied_job_ids

    return render(request, 'job_list.html', {
        'jobs': jobs, 
        'candidate_profile': candidate_profile
    })


def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    has_applied = False
    match_score = None
    if request.user.is_authenticated and request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        if candidate_profile is not None:
            has_applied = Application.objects.filter(candidate=candidate_profile, job=job).exists()
            match_score = calculate_match_score(candidate_profile, job)

    return render(request, 'job_detail.html', {
        'job': job, 
        'has_applied': has_applied,
        'match_score': match_score
    })


import json

@login_required
def job_create(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    all_skills = Skill.objects.all().order_by('category', 'skill_name')
    
    # Group skills by category for dynamic JS dropdowns
    skills_dict = {}
    for skill in all_skills:
        cat_name = skill.get_category_display()
        if cat_name not in skills_dict:
            skills_dict[cat_name] = []
        skills_dict[cat_name].append({'id': skill.pk, 'name': skill.skill_name})
    skills_json = json.dumps(skills_dict)

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiter_profile
            job.save()
            _save_skill_requirements(request, job)
            messages.success(request, 'Job post created successfully!')
            return redirect('job_skill_manage', pk=job.pk)
    else:
        form = JobPostForm()

    return render(request, 'job_form.html', {
        'form': form, 
        'skills_json': skills_json,
        'level_choices': JobSkillRequirement.LEVEL
    })


@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)

    if request.user.role != 'recruiter' or recruiter_profile != job.recruiter:
        messages.error(request, 'You are not allowed to edit this job post.')
        return redirect('job_detail', pk=job.pk)

    all_skills = Skill.objects.all().order_by('category', 'skill_name')
    
    skills_dict = {}
    for skill in all_skills:
        cat_name = skill.get_category_display()
        if cat_name not in skills_dict:
            skills_dict[cat_name] = []
        skills_dict[cat_name].append({'id': skill.pk, 'name': skill.skill_name})
    skills_json = json.dumps(skills_dict)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            _save_skill_requirements(request, job)
            messages.success(request, 'Job post updated successfully!')
            return redirect('job_skill_manage', pk=job.pk)
    else:
        form = JobPostForm(instance=job)

    return render(request, 'job_form.html', {
        'form': form, 
        'job': job, 
        'skills_json': skills_json,
        'level_choices': JobSkillRequirement.LEVEL
    })


def _save_skill_requirements(request, job):
    """Parse skill requirement fields from POST and save them."""
    skill_ids = request.POST.getlist('req_skill')[:3]
    levels = request.POST.getlist('req_level')[:3]
    for skill_id, level in zip(skill_ids, levels):
        if skill_id and level:
            JobSkillRequirement.objects.get_or_create(
                job=job,
                skill_id=skill_id,
                defaults={'required_level': level, 'is_mandatory': True}
            )


@login_required
def job_skill_manage(request, pk):
    """Manage required skills for a job post (add/remove inline)."""
    job = get_object_or_404(JobPost, pk=pk)
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)

    if request.user.role != 'recruiter' or recruiter_profile != job.recruiter:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        level = request.POST.get('required_level', 'beginner')
        if skill_id:
            JobSkillRequirement.objects.get_or_create(
                job=job,
                skill_id=skill_id,
                defaults={'required_level': level, 'is_mandatory': True}
            )
            messages.success(request, 'Required skill added.')
        return redirect('job_skill_manage', pk=pk)

    existing = job.skill_requirements.select_related('skill').all()
    all_skills = Skill.objects.exclude(
        id__in=existing.values_list('skill_id', flat=True)
    ).order_by('category', 'skill_name')

    return render(request, 'job_skill_manage.html', {
        'job': job,
        'existing': existing,
        'all_skills': all_skills,
        'level_choices': JobSkillRequirement.LEVEL,
    })


@login_required
def job_skill_delete(request, pk, skill_req_id):
    """Remove a required skill from a job post."""
    job = get_object_or_404(JobPost, pk=pk)
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)

    if request.user.role != 'recruiter' or recruiter_profile != job.recruiter:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    req = get_object_or_404(JobSkillRequirement, pk=skill_req_id, job=job)
    req.delete()
    messages.success(request, 'Required skill removed.')
    return redirect('job_skill_manage', pk=pk)


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
    return render(request, 'my_applications.html', {'applications': applications})


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

    match_score = calculate_match_score(candidate_profile, job)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = candidate_profile
            app.job = job
            app.match_score = match_score
            app.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {'form': form, 'job': job, 'match_score': match_score})

@login_required
def job_applicants(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    if request.user.role != 'recruiter' or job.recruiter != request.user.recruiter_profile:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    all_applicants = Application.objects.filter(job=job).select_related('candidate').order_by('-match_score')
    
    # Calculate stats on ALL applicants
    total_count = all_applicants.count()
    qualified_count = all_applicants.filter(match_score__gte=8.0).count()
    avg_score = 0
    if total_count > 0:
        avg_score = sum(a.match_score for a in all_applicants) / total_count

    return render(request, 'job_applicants.html', {
        'job': job, 
        'applicants': all_applicants,
        'total_count': total_count,
        'qualified_count': qualified_count,
        'avg_score': round(avg_score, 1)
    })

@login_required
def job_analysis(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    
    if request.user.role == 'recruiter':
        if job.recruiter != request.user.recruiter_profile:
            messages.error(request, 'Access denied.')
            return redirect('dashboard')
        applicants = Application.objects.filter(job=job).select_related('candidate').order_by('-match_score')
    elif request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        applicants = Application.objects.filter(job=job, candidate=candidate_profile).select_related('candidate')
        if not applicants.exists():
            messages.error(request, 'You have not applied for this job.')
            return redirect('job_detail', pk=pk)
    else:
        return redirect('dashboard')
    
    return render(request, 'job_analysis.html', {
        'job': job, 
        'applicants': applicants,
    })
