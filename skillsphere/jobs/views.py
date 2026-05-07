import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Notification
from interviews.forms import RecruiterInterviewInviteForm
from interviews.models import Interview
from skills.models import JobSkillRequirement, Skill

from jobs.forms import ApplicationForm, JobOfferForm, JobPostForm
from jobs.models import Application, JobOffer, JobPost
from jobs.utils import calculate_match_score


INTERVIEW_MATCH_THRESHOLD = 8.0


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
    skill_ids = request.POST.getlist("skill_id")
    levels = request.POST.getlist("required_level")

    if not skill_ids:
        skill_ids = request.POST.getlist("req_skill")
        levels = request.POST.getlist("req_level")

    if not skill_ids:
        skill_id = request.POST.get("skill_id")
        level = request.POST.get("required_level")
        if skill_id:
            skill_ids = [skill_id]
            levels = [level or "beginner"]

    for index, skill_id in enumerate(skill_ids):
        if not skill_id:
            continue
        JobSkillRequirement.objects.update_or_create(
            job=job,
            skill_id=skill_id,
            defaults={"required_level": levels[index] if index < len(levels) else "beginner"},
        )


def _refresh_job_match_scores(job):
    applications = Application.objects.filter(candidate__isnull=False, job=job).select_related("candidate")
    for application in applications:
        application.match_score = calculate_match_score(application.candidate, job)
        application.save(update_fields=["match_score", "updated_at"])


def job_list(request):
    jobs = list(JobPost.objects.filter(status="open").select_related("recruiter"))
    candidate_profile = None

    if request.user.is_authenticated and request.user.role == "candidate":
        candidate_profile = _get_candidate_profile(request.user)
        if candidate_profile:
            applied_job_ids = set(
                Application.objects.filter(candidate=candidate_profile).values_list(
                    "job_id", flat=True
                )
            )
            for job in jobs:
                job.match_score = calculate_match_score(candidate_profile, job)
                job.has_applied = job.id in applied_job_ids

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


def job_detail(request, pk):
    job = get_object_or_404(
        JobPost.objects.select_related("recruiter"), pk=pk
    )
    has_applied = False
    match_score = None

    if request.user.is_authenticated and request.user.role == "candidate":
        candidate_profile = _get_candidate_profile(request.user)
        if candidate_profile is not None:
            has_applied = Application.objects.filter(
                candidate=candidate_profile, job=job
            ).exists()
            match_score = calculate_match_score(candidate_profile, job)

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

    all_skills, skills_json = _build_skills_json()

    if request.method == "POST":
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


@login_required
def job_edit(request, pk):
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
            _refresh_job_match_scores(job)
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


@login_required
def apply_job(request, pk):
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
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = candidate_profile
            application.job = job
            application.match_score = match_score
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect("my_applications")
    else:
        form = ApplicationForm()

    return render(
        request,
        "apply.html",
        {"form": form, "job": job, "match_score": match_score},
    )


@login_required
def job_applicants(request, pk):
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != job.recruiter:
        messages.error(request, "You are not allowed to review applicants for this job.")
        return redirect("job_detail", pk=job.pk)

    _refresh_job_match_scores(job)
    applicants = list(
        Application.objects.filter(job=job)
        .select_related("candidate", "candidate__user", "job")
        .order_by("-match_score", "-applied_at")
    )

    total_count = len(applicants)
    qualified_count = len([app for app in applicants if app.match_score >= INTERVIEW_MATCH_THRESHOLD])
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
            "interview_threshold": INTERVIEW_MATCH_THRESHOLD,
        },
    )


@login_required
def job_analysis(request, pk):
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)

    if request.user.role == "recruiter":
        recruiter_profile = _get_recruiter_profile(request.user)
        if recruiter_profile != job.recruiter:
            messages.error(request, "You are not allowed to view this analysis.")
            return redirect("job_detail", pk=job.pk)

        _refresh_job_match_scores(job)
        applicants = list(
            Application.objects.filter(job=job)
            .select_related("candidate", "candidate__user")
            .order_by("-match_score", "-applied_at")
        )

        return render(
            request,
            "job_analysis.html",
            {"job": job, "applicants": applicants, "interview_threshold": INTERVIEW_MATCH_THRESHOLD},
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
            {"job": job, "applicants": [application], "interview_threshold": INTERVIEW_MATCH_THRESHOLD},
        )

    messages.error(request, "You are not allowed to view this analysis.")
    return redirect("job_detail", pk=job.pk)


@login_required
def call_for_interview(request, application_pk):
    application = get_object_or_404(
        Application.objects.select_related("candidate", "candidate__user", "job", "job__recruiter"),
        pk=application_pk,
    )
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != application.job.recruiter:
        messages.error(request, "You are not allowed to call this candidate for interview.")
        return redirect("dashboard")

    application.match_score = calculate_match_score(application.candidate, application.job)
    if application.match_score < INTERVIEW_MATCH_THRESHOLD:
        application.save(update_fields=["match_score", "updated_at"])
        messages.error(request, "This candidate needs a match score of 8.0 or higher before you can call them for interview.")
        return redirect("job_applicants", pk=application.job.pk)

    existing_interview = Interview.objects.filter(
        candidate=application.candidate,
        job=application.job,
    ).first()

    if request.method == "POST":
        form = RecruiterInterviewInviteForm(request.POST, instance=existing_interview)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.candidate = application.candidate
            interview.job = application.job
            interview.status = "scheduled"
            if not interview.interview_type:
                interview.interview_type = "hr"
            if not interview.round_number:
                interview.round_number = 1
            scheduled_time_value = interview.scheduled_time
            if hasattr(scheduled_time_value, "strftime"):
                interview.scheduled_time = scheduled_time_value.strftime("%H:%M")
            elif isinstance(scheduled_time_value, str):
                # Keep existing HH:MM strings and normalize HH:MM:SS values.
                try:
                    interview.scheduled_time = datetime.strptime(scheduled_time_value, "%H:%M:%S").strftime("%H:%M")
                except ValueError:
                    interview.scheduled_time = scheduled_time_value
            interview.save()

            application.status = "shortlisted"
            application.save(update_fields=["status", "match_score", "updated_at"])

            Notification.objects.update_or_create(
                user=application.candidate.user,
                interview=interview,
                defaults={
                    "title": "Interview Invitation",
                    "message": (
                        f"You have been selected for an interview for {application.job.title} "
                        f"at {application.job.recruiter.company_name}."
                    ),
                    "is_read": False,
                },
            )

            messages.success(request, f"Interview invitation sent to {application.candidate.full_name}.")
            return redirect("interview_detail", pk=interview.pk)
    else:
        form = RecruiterInterviewInviteForm(instance=existing_interview)

    return render(
        request,
        "call_for_interview.html",
        {
            "application": application,
            "job": application.job,
            "candidate": application.candidate,
            "form": form,
            "existing_interview": existing_interview,
        },
    )


@login_required
def job_skill_manage(request, pk):
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
            _refresh_job_match_scores(job)
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


@login_required
def job_skill_delete(request, pk, skill_req_id):
    job = get_object_or_404(JobPost.objects.select_related("recruiter"), pk=pk)
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != job.recruiter:
        messages.error(request, "You are not allowed to remove this skill.")
        return redirect("job_detail", pk=job.pk)

    requirement = get_object_or_404(JobSkillRequirement, pk=skill_req_id, job=job)

    if request.method == "POST":
        requirement.delete()
        _refresh_job_match_scores(job)
        messages.success(request, "Required skill removed.")

    return redirect("job_skill_manage", pk=job.pk)


@login_required
def send_job_offer(request, application_pk):
    application = get_object_or_404(
        Application.objects.select_related("candidate", "candidate__user", "job", "job__recruiter"),
        pk=application_pk,
    )
    recruiter_profile = _get_recruiter_profile(request.user)

    if request.user.role != "recruiter" or recruiter_profile != application.job.recruiter:
        messages.error(request, "You are not allowed to send a job offer for this application.")
        return redirect("dashboard")

    if JobOffer.objects.filter(candidate=application.candidate, job=application.job).exists():
        messages.info(request, f"An offer has already been sent to {application.candidate.full_name}.")
        return redirect("offer_list")

    if request.method == "POST":
        form = JobOfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.candidate = application.candidate
            offer.job = application.job
            offer.save()

            application.status = "offered"
            application.save(update_fields=["status", "updated_at"])

            Notification.objects.create(
                user=application.candidate.user,
                title="New Job Offer",
                message=(
                    f"Congratulations! You have received a job offer for {application.job.title} "
                    f"from {application.job.recruiter.company_name}."
                ),
            )

            messages.success(request, f"Job offer sent to {application.candidate.full_name}.")
            return redirect("offer_list")
    else:
        form = JobOfferForm()

    return render(
        request,
        "offer_form.html",
        {
            "form": form,
            "application": application,
            "job": application.job,
            "candidate": application.candidate,
        },
    )


@login_required
def offer_list(request):
    if request.user.role == "candidate":
        profile = _get_candidate_profile(request.user)
        offers = JobOffer.objects.filter(candidate=profile).select_related("job", "job__recruiter").order_by("-created_at")
        return render(request, "offer_list.html", {"offers": offers, "role": "candidate"})
    
    if request.user.role == "recruiter":
        profile = _get_recruiter_profile(request.user)
        offers = JobOffer.objects.filter(job__recruiter=profile).select_related("candidate", "job").order_by("-created_at")
        return render(request, "offer_list.html", {"offers": offers, "role": "recruiter"})

    return redirect("dashboard")


@login_required
def respond_to_offer(request, offer_pk):
    if request.method != "POST":
        return redirect("offer_list")

    offer = get_object_or_404(JobOffer.objects.select_related("candidate", "job", "job__recruiter"), pk=offer_pk)
    
    if request.user.role != "candidate" or offer.candidate.user != request.user:
        messages.error(request, "You are not authorized to respond to this offer.")
        return redirect("dashboard")

    if offer.offer_status != "pending":
        messages.error(request, "You have already responded to this offer.")
        return redirect("offer_list")

    action = request.POST.get("action")

    if action == "accepted":
        offer.offer_status = "accepted"
        offer.save()
        # Update application status to hired
        Application.objects.filter(candidate=offer.candidate, job=offer.job).update(status="hired")
        
        Notification.objects.create(
            user=offer.job.recruiter.user,
            title="Offer Accepted",
            message=f"{offer.candidate.full_name} has accepted the offer for {offer.job.title}."
        )
        messages.success(request, "Offer accepted successfully!")
    elif action == "rejected":
        offer.offer_status = "rejected"
        offer.save()
        # Update application status to rejected
        Application.objects.filter(candidate=offer.candidate, job=offer.job).update(status="rejected")
        
        Notification.objects.create(
            user=offer.job.recruiter.user,
            title="Offer Rejected",
            message=f"{offer.candidate.full_name} has rejected the offer for {offer.job.title}."
        )
        messages.info(request, "Offer rejected.")
    else:
        messages.error(request, "Invalid action.")

    return redirect("offer_list")


