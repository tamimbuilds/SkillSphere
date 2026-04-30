from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Skill, Question, CandidateSkill, Certificate, Assessment, Score, JobSkillRequirement
from .forms import (
    SkillForm,
    CandidateSkillForm,
    CertificateForm,
    JobSkillRequirementForm
)

ASSESSMENT_TIME_LIMIT_MINUTES = 10


def _assessment_timer_session_key(candidate_skill_id, attempt_number):
    return f'assessment_started_{candidate_skill_id}_{attempt_number}'


# ---------------- SKILL ----------------

def skill_list(request):
    skills = Skill.objects.all()
    return render(request, 'skill_list.html', {'skills': skills})


def add_skill(request):
    form = SkillForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('skill_list')
    return render(request, 'add_skill.html', {'form': form})


def edit_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    form = SkillForm(request.POST or None, instance=skill)
    if form.is_valid():
        form.save()
        return redirect('skill_list')
    return render(request, 'add_skill.html', {'form': form})


def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    return redirect('skill_list')


# ---------------- CANDIDATE SKILL ----------------

@login_required
def candidate_skill_list(request):
    if request.user.role != 'candidate':
        return redirect('home')
    
    from accounts.models import CandidateProfile
    profile, created = CandidateProfile.objects.get_or_create(
        user=request.user,
        defaults={'full_name': request.user.get_full_name() or request.user.username}
    )
    sector = profile.specialized_sector
    my_skills = CandidateSkill.objects.filter(candidate=profile).select_related('skill')
    
    for s in my_skills:
        score_qs = Score.objects.filter(user=request.user, candidate_skill=s).order_by('-attempt_number', '-completed_at')
        s.latest_score = score_qs.first()
        s.attempt_count = score_qs.count()
        s.has_assessment = s.latest_score is not None
        s.can_retry = s.attempt_count < 3 and not (s.latest_score and s.latest_score.passed)
        
    all_skills = Skill.objects.all().order_by('category', 'skill_name')
    
    # Handle Skill Addition on the same page
    form = CandidateSkillForm(request.POST or None, sector=sector)
    
    if request.method == 'POST' and form.is_valid():
        skill_obj = form.save(commit=False)
        skill_obj.candidate = profile
        
        # Security check: ensure the skill belongs to their sector
        if not sector:
            messages.error(request, "Please select a specialized sector in your profile before adding skills.")
        elif skill_obj.skill.category != sector:
            messages.error(request, "You can only add skills within your specialized sector.")
        else:
            try:
                skill_obj.save()
                messages.success(request, f'Skill "{skill_obj.skill.skill_name}" added successfully! Note: You haven\'t taken an assessment for this skill yet.')
                return redirect('my_skills')
            except Exception as e:
                messages.error(request, str(e))
    
    return render(request, 'my_skills.html', {
        'form': form,
        'data': my_skills,
        'all_skills': all_skills,
        'user_sector': sector
    })


@login_required
def delete_candidate_skill(request, pk):
    from accounts.models import CandidateProfile
    profile = get_object_or_404(CandidateProfile, user=request.user)
    skill = get_object_or_404(CandidateSkill, pk=pk, candidate=profile)
    skill_name = skill.skill.skill_name
    skill.delete()
    messages.info(request, f'Skill "{skill_name}" removed from your profile.')
    return redirect('my_skills')


# ---------------- CERTIFICATE ----------------

def certificate_list(request):
    certificates = Certificate.objects.all()
    return render(request, 'certificate_list.html', {'certificates': certificates})


def add_certificate(request, pk):
    form = CertificateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        cert = form.save(commit=False)
        cert.candidate_skill_id = pk
        cert.save()
        return redirect('certificate_list')
    return render(request, 'certificate_form.html', {'form': form})


def verify_certificate(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    certificate.verification_status = 'verified'
    certificate.verified_by_admin = True
    certificate.save()
    return redirect('certificate_list')


# ---------------- ASSESSMENT ----------------

@login_required
def assessment_list(request):
    if request.user.role != 'candidate':
        return redirect('home')

    scores = Score.objects.filter(user=request.user).select_related('candidate_skill', 'candidate_skill__skill').order_by(
        'candidate_skill__skill__skill_name', '-attempt_number'
    )
    return render(request, 'assessment.html', {'scores': scores})


@login_required
def add_assessment(request, pk):
    from accounts.models import CandidateProfile
    profile = get_object_or_404(CandidateProfile, user=request.user)
    skill = get_object_or_404(CandidateSkill, pk=pk, candidate=profile)
    previous_scores = list(
        Score.objects.filter(user=request.user, candidate_skill=skill).order_by('attempt_number', 'completed_at')
    )
    latest_score = previous_scores[-1] if previous_scores else None
    attempt_count = len(previous_scores)

    if latest_score and latest_score.passed:
        messages.info(request, f'You already passed the assessment for {skill.skill.skill_name}.')
        return redirect('my_skills')

    if attempt_count >= 3:
        messages.error(request, f'You have already used all 3 attempts for {skill.skill.skill_name}.')
        return redirect('my_skills')

    next_attempt = attempt_count + 1
    next_set_number = next_attempt
    timer_session_key = _assessment_timer_session_key(skill.pk, next_attempt)
    questions = list(
        Question.objects.filter(skill=skill.skill, set_number=next_set_number, is_active=True).order_by('question_order', 'id')
    )

    if len(questions) < 10:
        messages.error(
            request,
            f"{skill.skill.skill_name} is missing question set {next_set_number}. Please add 10 questions for that set."
        )
        return redirect('my_skills')

    started_at_iso = request.session.get(timer_session_key)
    if started_at_iso:
        started_at = datetime.fromisoformat(started_at_iso)
        if timezone.is_naive(started_at):
            started_at = timezone.make_aware(started_at, timezone.get_current_timezone())
    else:
        started_at = timezone.now()
        request.session[timer_session_key] = started_at.isoformat()

    expires_at = started_at + timedelta(minutes=ASSESSMENT_TIME_LIMIT_MINUTES)

    if request.method == 'POST':
        if timezone.now() > expires_at:
            request.session.pop(timer_session_key, None)
            messages.error(
                request,
                f'Time expired for {skill.skill.skill_name}. The 10-minute limit has passed for attempt {next_attempt}/3.'
            )
            return redirect('my_skills')

        missing_answers = [q for q in questions if not request.POST.get(f'question_{q.pk}')]
        if missing_answers:
            messages.error(request, 'Please answer all 10 questions before submitting the assessment.')
        else:
            correct_answers = 0
            total_questions = len(questions)
            percentage = 0
            passed = False

            score_record = Score.objects.create(
                user=request.user,
                candidate_skill=skill,
                attempt_number=next_attempt,
                question_set_number=next_set_number,
                total_questions=total_questions,
                correct_answers=0,
                score=0,
                passed=False,
            )

            for question in questions:
                user_answer = request.POST.get(f'question_{question.pk}')
                is_correct = user_answer == question.correct_option
                if is_correct:
                    correct_answers += 1

                Assessment.objects.create(
                    user=request.user,
                    candidate_skill=skill,
                    score_record=score_record,
                    question=question,
                    user_answer=user_answer,
                    is_correct=is_correct,
                )

            percentage = round((correct_answers / total_questions) * 100, 2)
            passed = correct_answers >= 6
            score_record.correct_answers = correct_answers
            score_record.score = percentage
            score_record.passed = passed
            score_record.save(update_fields=['correct_answers', 'score', 'passed', 'completed_at'])

            skill.verified = passed
            skill.save(update_fields=['verified'])
            
            # Update match scores for all applications
            from jobs.utils import update_candidate_match_scores
            update_candidate_match_scores(profile)

            request.session.pop(timer_session_key, None)

            status_text = 'passed' if passed else 'completed'
            messages.success(
                request,
                f'Assessment {status_text} for {skill.skill.skill_name}. Attempt {next_attempt}/3, set {next_set_number}, score {correct_answers}/{total_questions} ({percentage}%).'
            )
            return redirect('my_skills')

    return render(request, 'assessment_form.html', {
        'candidate_skill': skill,
        'skill_name': skill.skill.skill_name,
        'questions': questions,
        'attempt_number': next_attempt,
        'set_number': next_set_number,
        'remaining_attempts': 4 - next_attempt,
        'time_limit_minutes': ASSESSMENT_TIME_LIMIT_MINUTES,
        'expires_at_unix_ms': int(expires_at.timestamp() * 1000),
    })


# ---------------- JOB SKILL REQUIREMENT ----------------

def job_skill_requirement_list(request):
    data = JobSkillRequirement.objects.all()
    return render(request, 'job_skill_requirement_list.html', {'data': data})


def add_job_skill_requirement(request):
    form = JobSkillRequirementForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('job_skill_requirement_list')
    return render(request, 'job_skill_requirement_form.html', {'form': form})

