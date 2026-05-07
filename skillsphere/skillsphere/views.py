from django.shortcuts import render
from accounts.models import CandidateProfile
from jobs.models import JobPost, Application
from skills.models import CandidateSkill, Score, Skill
from interviews.models import Interview


def home(request):
    # ── Platform Stats ──────────────────────────────────────────
    total_candidates = CandidateProfile.objects.count()
    total_jobs = JobPost.objects.count()
    total_skills = Skill.objects.count()

    hero_stats = {
        'Candidates': f"{total_candidates:,}+",
        'Active Jobs': f"{total_jobs:,}+",
        'Skills Certified': f"{total_skills:,}+",
    }

    # ── Featured Candidates (up to 6, those who have skills) ────
    candidate_profiles = CandidateProfile.objects.select_related('user').order_by('-id')[:20]
    featured_candidates = []
    for profile in candidate_profiles:
        skills = CandidateSkill.objects.filter(candidate=profile).select_related('skill')[:3]
        if not skills:
            continue
        for s in skills:
            score_qs = Score.objects.filter(
                user=profile.user, candidate_skill=s
            ).order_by('-attempt_number', '-completed_at')
            s.latest_score = score_qs.first()
            s.has_assessment = s.latest_score is not None
        featured_candidates.append({'profile': profile, 'skills': skills})
        if len(featured_candidates) >= 6:
            break

    # ── Featured Skills (most popular) ──────────────────────────
    from django.db.models import Count
    skill_counts = (
        CandidateSkill.objects
        .values('skill__skill_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    palette = ['#c9a96e', '#1a1a2e', '#1a7a4a', '#1a4f8c', '#b8860b']
    featured_skills = [
        (item['skill__skill_name'], min(100, item['count'] * 12 + 30), palette[i])
        for i, item in enumerate(skill_counts)
    ]

    context = {
        'hero_stats': hero_stats,
        'featured_candidates': featured_candidates,
        'featured_skills': featured_skills,
    }
    return render(request, 'home.html', context)
