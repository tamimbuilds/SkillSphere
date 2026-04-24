from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, CandidateSkill, Certificate, Assessment, JobSkillRequirement
from .forms import (
    SkillForm,
    CandidateSkillForm,
    CertificateForm,
    AssessmentForm,
    JobSkillRequirementForm
)

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
    my_skills = CandidateSkill.objects.filter(candidate=profile)
    
    # Check assessment status for each skill
    for s in my_skills:
        s.has_assessment = Assessment.objects.filter(candidate_skill=s).exists()
        
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

def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'assessment.html', {'assessments': assessments})


def add_assessment(request, pk):
    from accounts.models import CandidateProfile
    profile = get_object_or_404(CandidateProfile, user=request.user)
    skill = get_object_or_404(CandidateSkill, pk=pk, candidate=profile)
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.candidate_skill = skill
            obj.save()
            messages.success(request, f'Assessment for {skill.skill.skill_name} completed successfully!')
            return redirect('my_skills')
    else:
        form = AssessmentForm()
    
    return render(request, 'assessment_form.html', {
        'form': form,
        'skill_name': skill.skill.skill_name
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