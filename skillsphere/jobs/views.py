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

    recruiter_profile = getattr(request.user, 'recruiter_profile', None)
    if recruiter_profile is None:
        messages.error(request, 'Please complete your recruiter profile before posting a job.')
        return redirect('profile')

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
            job.recruiter = recruiter_profile
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
        form = JobPostForm(request)