from accounts.models import CandidateProfile
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.db.utils import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render
from jobs.models import JobPost
from skills.models import CandidateSkill, Score, Skill

ESSENTIAL_TABLES = {'django_migrations', 'accounts_user'}


def health(request):
    try:
        connection = connections[DEFAULT_DB_ALIAS]
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()

        existing_tables = set(connection.introspection.table_names())
        if missing_tables := sorted(ESSENTIAL_TABLES - existing_tables):
            return HttpResponse(
                f"database not migrated: missing {', '.join(missing_tables)}",
                content_type='text/plain',
                status=503,
            )

        executor = MigrationExecutor(connection)
        targets = executor.loader.graph.leaf_nodes()
        if executor.migration_plan(targets):
            return HttpResponse('pending migrations', content_type='text/plain', status=503)
    except DatabaseError:
        return HttpResponse('database unavailable', content_type='text/plain', status=503)

    return HttpResponse('ok', content_type='text/plain')


def _build_home_context():
    context = {
        'hero_stats': {
            'Candidates': '0+',
            'Active Jobs': '0+',
            'Skills Certified': '0+',
        },
        'featured_candidates': [],
        'featured_skills': [],
    }

    total_candidates = CandidateProfile.objects.count()
    total_jobs = JobPost.objects.count()
    total_skills = Skill.objects.count()

    context['hero_stats'] = {
        'Candidates': f"{total_candidates:,}+",
        'Active Jobs': f"{total_jobs:,}+",
        'Skills Certified': f"{total_skills:,}+",
    }

    candidate_profiles = CandidateProfile.objects.select_related('user').order_by('-id')[:20]
    featured_candidates = []
    for profile in candidate_profiles:
        candidate_skills = CandidateSkill.objects.filter(candidate=profile).select_related('skill')[:3]
        if not candidate_skills:
            continue

        for candidate_skill in candidate_skills:
            latest_score = (
                Score.objects.filter(user=profile.user, candidate_skill=candidate_skill)
                .order_by('-attempt_number', '-completed_at')
                .first()
            )
            candidate_skill.latest_score = latest_score
            candidate_skill.has_assessment = latest_score is not None

        featured_candidates.append({'profile': profile, 'skills': candidate_skills})
        if len(featured_candidates) >= 6:
            break

    from django.db.models import Count

    skill_counts = (
        CandidateSkill.objects
        .values('skill__skill_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    palette = ['#c9a96e', '#1a1a2e', '#1a7a4a', '#1a4f8c', '#b8860b']

    context['featured_candidates'] = featured_candidates
    context['featured_skills'] = [
        (item['skill__skill_name'], min(100, item['count'] * 12 + 30), palette[i])
        for i, item in enumerate(skill_counts)
    ]
    return context


def home(request):
    try:
        context = _build_home_context()
    except DatabaseError:
        context = {
            'hero_stats': {
                'Candidates': '0+',
                'Active Jobs': '0+',
                'Skills Certified': '0+',
            },
            'featured_candidates': [],
            'featured_skills': [],
        }

    return render(request, 'home.html', context)
