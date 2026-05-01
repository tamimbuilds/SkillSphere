import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

<<<<<<< HEAD
=======
from accounts.models import Notification
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b
from skills.models import JobSkillRequirement, Skill

from .forms import ApplicationForm, JobPostForm
from .models import Application, JobPost
from .utils import calculate_match_score


<<<<<<< HEAD
def _get_recruiter_profile(user):
    return getattr(user, "recruiter_profile", None)


def _get_candidate_profile(user):
    return getattr(user, "candidate_profile", None)


def _build_skills_json():
    all_skills = Skill.objects.all().order_by("category", "skill_name")
    skills_dict = {}
    for skill in all_skills:
        category_name = skill.get_category_display()
        skills_dict.setdefault(category_name, []).append(
            {"id": skill.pk, "name": skill.skill_name}
        )
    return all_skills, json.dumps(skills_dict)


def _save_skill_requirements(request, job):
    skill_ids = request.POST.getlist("req_skill")
    levels = request.POST.getlist("req_level")

    for skill_id, level in zip(skill_ids, levels):
        if not skill_id:
            continue
        JobSkillRequirement.objects.get_or_create(
            job=job,
            skill_id=skill_id,
            defaults={"required_level": level or "beginner"},
        )
=======
INTERVIEW_MATCH_THRESHOLD = 8.0


def _skills_json():
    skills_dict = {}
    for skill in Skill.objects.all().order_by('category', 'skill_name'):
        cat_name = skill.get_category_display()
        skills_dict.setdefault(cat_name, []).append({'id': skill.pk, 'name': skill.skill_name})
    return json.dumps(skills_dict)


def _save_skill_requirements(request, job):
    skill_ids = request.POST.getlist('skill_id')
    levels = request.POST.getlist('required_level')

    if not skill_ids:
        skill_ids = request.POST.getlist('req_skill')
        levels = request.POST.getlist('req_level')

    if not skill_ids:
        skill_id = request.POST.get('skill_id')
        level = request.POST.get('required_level')
        if skill_id:
            skill_ids = [skill_id]
            levels = [level or 'beginner']

    for index, skill_id in enumerate(skill_ids):
        if not skill_id:
            continue
        JobSkillRequirement.objects.update_or_create(
            job=job,
            skill_id=skill_id,
            defaults={'required_level': levels[index] if index < len(levels) else 'beginner'},
        )


def _refresh_job_match_scores(job):
    applications = Application.objects.filter(candidate__isnull=False, job=job).select_related('candidate')
    for application in applications:
        application.match_score = calculate_match_score(application.candidate, job)
        application.save(update_fields=['match_score', 'updated_at'])


def _owned_job_or_redirect(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)
    if request.user.role != 'recruiter' or recruiter_profile != job.recruiter:
        messages.error(request, 'You are not allowed to manage this job post.')
        return None
    return job
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


def job_list(request):
    jobs = list(JobPost.objects.filter(status="open").select_related("recruiter"))
    candidate_profile = None

<<<<<<< HEAD
    if request.user.is_authenticated and request.user.role == "candidate":
        candidate_profile = _get_candidate_profile(request.user)
=======
    if request.user.is_authenticated and request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b
        if candidate_profile:
            applied_job_ids = set(
                Application.objects.filter(candidate=candidate_profile).values_list(
                    "job_id", flat=True
                )
            )
            for job in jobs:
                job.match_score = calculate_match_score(candidate_profile, job)
                job.has_applied = job.id in applied_job_ids

<<<<<<< HEAD
    return render(
        request,
        "job_list.html",
        {
            "jobs": jobs,
            "candidate_profile": candidate_profile,
        },
    )


@login_required
def dashboard(request):
    if request.user.role == "candidate":
        candidate_profile = _get_candidate_profile(request.user)
        applications = []
        if candidate_profile:
            applications = list(
                Application.objects.filter(candidate=candidate_profile)
                .select_related("job", "job__recruiter")
                .order_by("-applied_at")
            )
            for app in applications:
                app.match_score = calculate_match_score(candidate_profile, app.job)
        return render(
            request,
            "dashboard.html",
            {"role": "candidate", "applications": applications},
        )

    if request.user.role == "recruiter":
        recruiter_profile = _get_recruiter_profile(request.user)
        jobs = []
        if recruiter_profile:
            jobs = list(
                JobPost.objects.filter(recruiter=recruiter_profile).order_by("-posted_at")
            )
        return render(request, "dashboard.html", {"role": "recruiter", "jobs": jobs})

    messages.error(request, "Unsupported user role.")
    return redirect("home")
=======
    return render(request, 'job_list.html', {
        'jobs': jobs,
        'candidate_profile': candidate_profile,
    })
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


def job_detail(request, pk):
    job = get_object_or_404(
        JobPost.objects.select_related("recruiter"), pk=pk
    )
    has_applied = False
    match_score = None

<<<<<<< HEAD
    if request.user.is_authenticated and request.user.role == "candidate":
        candidate_profile = _get_candidate_profile(request.user)
=======
    if request.user.is_authenticated and request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b
        if candidate_profile is not None:
            has_applied = Application.objects.filter(
                candidate=candidate_profile, job=job
            ).exists()
            match_score = calculate_match_score(candidate_profile, job)

<<<<<<< HEAD
    return render(
        request,
        "job_detail.html",
        {
            "job": job,
            "has_applied": has_applied,
            "match_score": match_score,
        },
    )


@login_required
def my_applications(request):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can view applications.")
        return redirect("dashboard")

    candidate_profile = _get_candidate_profile(request.user)
    if candidate_profile is None:
        messages.error(request, "Please complete your candidate profile first.")
        return redirect("profile")

    applications = list(
        Application.objects.filter(candidate=candidate_profile)
        .select_related("job", "job__recruiter")
        .order_by("-applied_at")
    )
    for app in applications:
        app.match_score = calculate_match_score(candidate_profile, app.job)

    return render(request, "my_applications.html", {"applications": applications})
=======
    return render(request, 'job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'match_score': match_score,
    })


@login_required
def dashboard(request):
    if request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        applications = Application.objects.filter(candidate=candidate_profile).select_related('job', 'job__recruiter')
        return render(request, 'dashboard.html', {
            'role': request.user.role,
            'applications': applications,
        })

    recruiter_profile = getattr(request.user, 'recruiter_profile', None)
    jobs = JobPost.objects.filter(recruiter=recruiter_profile).prefetch_related('skill_requirements')
    return render(request, 'dashboard.html', {
        'role': request.user.role,
        'jobs': jobs,
    })
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def job_create(request):
    if request.user.role != "recruiter":
        return redirect("job_list")

    recruiter_profile = _get_recruiter_profile(request.user)
    if recruiter_profile is None:
        messages.error(
            request, "Please complete your recruiter profile before posting a job."
        )
        return redirect("profile")

<<<<<<< HEAD
    all_skills, skills_json = _build_skills_json()

    if request.method == "POST":
=======
    if request.method == 'POST':
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = recruiter_profile
            job.save()
            _save_skill_requirements(request, job)
            messages.success(request, "Job post created successfully.")
            return redirect("job_skill_manage", pk=job.pk)
    else:
        form = JobPostForm()

<<<<<<< HEAD
    return render(
        request,
        "job_form.html",
        {
            "form": form,
            "skills_json": skills_json,
            "all_skills": all_skills,
            "level_choices": JobSkillRequirement.LEVEL,
        },
    )
=======
    return render(request, 'job_form.html', {
        'form': form,
        'skills_json': _skills_json(),
        'level_choices': JobSkillRequirement.LEVEL,
    })
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def job_edit(request, pk):
<<<<<<< HEAD
    job = get_object_or_404(JobPost, pk=pk)
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != job.recruiter:
        messages.error(request, "You are not allowed to edit this job post.")
        return redirect("job_detail", pk=job.pk)

    _, skills_json = _build_skills_json()

    if request.method == "POST":
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job post updated successfully.")
            return redirect("job_detail", pk=job.pk)
    else:
        form = JobPostForm(instance=job)

    return render(
        request,
        "job_form.html",
        {
            "form": form,
            "job": job,
            "skills_json": skills_json,
            "level_choices": JobSkillRequirement.LEVEL,
        },
    )
=======
    job = _owned_job_or_redirect(request, pk)
    if job is None:
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            _refresh_job_match_scores(job)
            messages.success(request, 'Job post updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobPostForm(instance=job)

    return render(request, 'job_form.html', {
        'form': form,
        'job': job,
        'skills_json': _skills_json(),
        'level_choices': JobSkillRequirement.LEVEL,
    })
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def apply_job(request, pk):
<<<<<<< HEAD
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can apply for jobs.")
        return redirect("job_detail", pk=pk)

    candidate_profile = _get_candidate_profile(request.user)
    if candidate_profile is None:
        messages.error(request, "Please complete your candidate profile first.")
        return redirect("profile")

    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)

    if Application.objects.filter(candidate=candidate_profile, job=job).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect("job_detail", pk=job.pk)

    match_score = calculate_match_score(candidate_profile, job)

    if request.method == "POST":
=======
    if request.user.role != 'candidate':
        messages.error(request, 'Only candidates can apply to jobs.')
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(JobPost, pk=pk, status='open')
    candidate_profile = getattr(request.user, 'candidate_profile', None)
    if candidate_profile is None:
        messages.error(request, 'Please complete your candidate profile before applying.')
        return redirect('profile')

    if Application.objects.filter(candidate=candidate_profile, job=job).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('my_applications')

    match_score = calculate_match_score(candidate_profile, job)
    if request.method == 'POST':
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = candidate_profile
            application.job = job
            application.match_score = match_score
            application.save()
<<<<<<< HEAD
            messages.success(request, "Application submitted successfully.")
            return redirect("my_applications")
    else:
        form = ApplicationForm()

    return render(
        request,
        "apply.html",
        {"form": form, "job": job, "match_score": match_score},
    )
=======
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'apply.html', {
        'form': form,
        'job': job,
        'match_score': match_score,
    })


@login_required
def my_applications(request):
    if request.user.role != 'candidate':
        return redirect('dashboard')

    candidate_profile = getattr(request.user, 'candidate_profile', None)
    applications = Application.objects.filter(candidate=candidate_profile).select_related('job', 'job__recruiter')
    return render(request, 'my_applications.html', {'applications': applications})
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def job_applicants(request, pk):
<<<<<<< HEAD
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != job.recruiter:
        messages.error(request, "You are not allowed to review applicants for this job.")
        return redirect("job_detail", pk=job.pk)

    applicants = list(
        Application.objects.filter(job=job)
        .select_related("candidate", "candidate__user", "job")
        .order_by("-match_score", "-applied_at")
    )

    for app in applicants:
        app.match_score = calculate_match_score(app.candidate, job)

    total_count = len(applicants)
    qualified_count = len([app for app in applicants if app.match_score >= 8])
    avg_score = round(
        sum(app.match_score for app in applicants) / total_count, 1
    ) if total_count else 0

    return render(
        request,
        "job_applicants.html",
        {
            "job": job,
            "applicants": applicants,
            "total_count": total_count,
            "qualified_count": qualified_count,
            "avg_score": avg_score,
        },
    )
=======
    job = _owned_job_or_redirect(request, pk)
    if job is None:
        return redirect('dashboard')

    _refresh_job_match_scores(job)
    applicants = Application.objects.filter(job=job).select_related('candidate', 'candidate__user').order_by('-match_score', 'applied_at')
    avg_score = applicants.aggregate(value=Avg('match_score'))['value'] or 0

    return render(request, 'job_applicants.html', {
        'job': job,
        'applicants': applicants,
        'total_count': applicants.count(),
        'avg_score': round(avg_score, 1),
        'qualified_count': applicants.filter(match_score__gte=INTERVIEW_MATCH_THRESHOLD).count(),
        'interview_threshold': INTERVIEW_MATCH_THRESHOLD,
    })
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def job_analysis(request, pk):
<<<<<<< HEAD
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)

    if request.user.role == "recruiter":
        recruiter_profile = _get_recruiter_profile(request.user)
        if recruiter_profile != job.recruiter:
            messages.error(request, "You are not allowed to view this analysis.")
            return redirect("job_detail", pk=job.pk)

        applicants = list(
            Application.objects.filter(job=job)
            .select_related("candidate", "candidate__user")
            .order_by("-match_score", "-applied_at")
        )
        for app in applicants:
            app.match_score = calculate_match_score(app.candidate, job)

        return render(
            request,
            "job_analysis.html",
            {"job": job, "applicants": applicants},
        )

    if request.user.role == "candidate":
        candidate_profile = _get_candidate_profile(request.user)
        application = get_object_or_404(
            Application.objects.select_related("candidate", "candidate__user"),
            candidate=candidate_profile,
            job=job,
        )
        application.match_score = calculate_match_score(candidate_profile, job)
        return render(
            request,
            "job_analysis.html",
            {"job": job, "applicants": [application]},
        )

    messages.error(request, "You are not allowed to view this analysis.")
    return redirect("job_detail", pk=job.pk)
=======
    job = get_object_or_404(JobPost, pk=pk)

    if request.user.role == 'recruiter':
        if getattr(request.user, 'recruiter_profile', None) != job.recruiter:
            messages.error(request, 'You are not allowed to view this analysis.')
            return redirect('dashboard')
        _refresh_job_match_scores(job)
        applicants = Application.objects.filter(job=job).select_related('candidate').order_by('-match_score')
    elif request.user.role == 'candidate':
        candidate_profile = getattr(request.user, 'candidate_profile', None)
        applicants = Application.objects.filter(candidate=candidate_profile, job=job).select_related('candidate')
    else:
        applicants = Application.objects.none()

    return render(request, 'job_analysis.html', {
        'job': job,
        'applicants': applicants,
        'interview_threshold': INTERVIEW_MATCH_THRESHOLD,
    })


@login_required
def call_for_interview(request, application_pk):
    application = get_object_or_404(
        Application.objects.select_related('candidate', 'candidate__user', 'job', 'job__recruiter'),
        pk=application_pk,
    )
    recruiter_profile = getattr(request.user, 'recruiter_profile', None)

    if request.user.role != 'recruiter' or recruiter_profile != application.job.recruiter:
        messages.error(request, 'You are not allowed to call this candidate for interview.')
        return redirect('dashboard')

    application.match_score = calculate_match_score(application.candidate, application.job)
    if application.match_score < INTERVIEW_MATCH_THRESHOLD:
        application.save(update_fields=['match_score', 'updated_at'])
        messages.error(request, 'This candidate needs a match score of 8.0 or higher before you can call them for interview.')
        return redirect('job_applicants', pk=application.job.pk)

    application.status = 'shortlisted'
    application.save(update_fields=['status', 'match_score', 'updated_at'])

    Notification.objects.create(
        user=application.candidate.user,
        title='Interview Invitation',
        message=(
            f'{application.job.recruiter.company_name} has called you for an interview '
            f'for the {application.job.title} role. Please watch this Notifications page for the next update.'
        ),
    )

    messages.success(request, f'{application.candidate.full_name} has been notified for interview.')
    return redirect('job_applicants', pk=application.job.pk)
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def job_skill_manage(request, pk):
<<<<<<< HEAD
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != job.recruiter:
        messages.error(request, "You are not allowed to edit this job's skills.")
        return redirect("job_detail", pk=job.pk)

    existing = list(
        JobSkillRequirement.objects.filter(job=job).select_related("skill")
    )
    existing_skill_ids = [req.skill_id for req in existing]

    if request.method == "POST":
        skill_id = request.POST.get("skill_id")
        required_level = request.POST.get("required_level") or "beginner"

        if not skill_id:
            messages.error(request, "Please select a skill.")
        elif JobSkillRequirement.objects.filter(job=job, skill_id=skill_id).exists():
            messages.info(request, "That skill is already added.")
        else:
            JobSkillRequirement.objects.create(
                job=job,
                skill_id=skill_id,
                required_level=required_level,
            )
            messages.success(request, "Required skill added.")
            return redirect("job_skill_manage", pk=job.pk)

    all_skills = Skill.objects.exclude(pk__in=existing_skill_ids).order_by(
        "category", "skill_name"
    )

    return render(
        request,
        "job_skill_manage.html",
        {
            "job": job,
            "existing": existing,
            "all_skills": all_skills,
            "level_choices": JobSkillRequirement.LEVEL,
        },
    )
=======
    job = _owned_job_or_redirect(request, pk)
    if job is None:
        return redirect('dashboard')

    if request.method == 'POST':
        _save_skill_requirements(request, job)
        _refresh_job_match_scores(job)
        messages.success(request, 'Required skill added.')
        return redirect('job_skill_manage', pk=job.pk)

    existing = JobSkillRequirement.objects.filter(job=job).select_related('skill').order_by('skill__category', 'skill__skill_name')
    existing_skill_ids = existing.values_list('skill_id', flat=True)
    all_skills = Skill.objects.exclude(pk__in=existing_skill_ids).order_by('category', 'skill_name')

    return render(request, 'job_skill_manage.html', {
        'job': job,
        'existing': existing,
        'all_skills': all_skills,
        'level_choices': JobSkillRequirement.LEVEL,
    })
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b


@login_required
def job_skill_delete(request, pk, skill_req_id):
<<<<<<< HEAD
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != job.recruiter:
        messages.error(request, "You are not allowed to remove this skill.")
        return redirect("job_detail", pk=job.pk)

    requirement = get_object_or_404(JobSkillRequirement, pk=skill_req_id, job=job)

    if request.method == "POST":
        requirement.delete()
        messages.success(request, "Required skill removed.")

    return redirect("job_skill_manage", pk=job.pk)
=======
    job = _owned_job_or_redirect(request, pk)
    if job is None:
        return redirect('dashboard')

    if request.method == 'POST':
        get_object_or_404(JobSkillRequirement, pk=skill_req_id, job=job).delete()
        _refresh_job_match_scores(job)
        messages.success(request, 'Required skill removed.')

    return redirect('job_skill_manage', pk=job.pk)
>>>>>>> 8e0500e8eeac2a190d1bbf2045ae5190ed94597b
