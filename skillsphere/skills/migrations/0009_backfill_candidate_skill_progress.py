from datetime import timedelta

from django.db import migrations
from django.utils import timezone


def backfill_candidate_skill_progress(apps, schema_editor):
    CandidateSkill = apps.get_model('skills', 'CandidateSkill')
    CandidateSkillProgress = apps.get_model('skills', 'CandidateSkillProgress')
    Score = apps.get_model('skills', 'Score')

    for candidate_skill in CandidateSkill.objects.all().iterator():
        scores = list(
            Score.objects.filter(candidate_skill_id=candidate_skill.id)
            .order_by('attempt_number', 'completed_at')
            .values('passed', 'completed_at')
        )
        progress, _ = CandidateSkillProgress.objects.get_or_create(
            candidate_id=candidate_skill.candidate_id,
            skill_id=candidate_skill.skill_id,
            defaults={'add_count': 1},
        )

        total_attempts = len(scores)
        total_failures = sum(1 for score in scores if not score['passed'])
        consecutive_failures = 0
        for score in reversed(scores):
            if score['passed']:
                break
            consecutive_failures += 1

        inferred_blocks = total_failures // 3
        latest_score = scores[-1] if scores else None
        blocked_until = progress.blocked_until
        if inferred_blocks and latest_score and not latest_score['passed']:
            latest_completed_at = latest_score['completed_at'] or timezone.now()
            candidate_blocked_until = latest_completed_at + timedelta(days=7)
            if not blocked_until or candidate_blocked_until > blocked_until:
                blocked_until = candidate_blocked_until

        progress.add_count = max(progress.add_count, 1)
        progress.total_attempts = max(progress.total_attempts, total_attempts)
        progress.total_failures = max(progress.total_failures, total_failures)
        progress.consecutive_failures = max(progress.consecutive_failures, consecutive_failures)
        progress.times_blocked = max(progress.times_blocked, inferred_blocks)
        progress.penalty_points = max(progress.penalty_points, round(inferred_blocks * 0.5, 2))
        progress.blocked_until = blocked_until
        progress.current_cycle_attempts = 0 if blocked_until and blocked_until > timezone.now() else total_attempts % 3
        progress.last_attempt_at = latest_score['completed_at'] if latest_score else progress.last_attempt_at
        progress.save()


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0008_unique_candidate_skill'),
    ]

    operations = [
        migrations.RunPython(backfill_candidate_skill_progress, migrations.RunPython.noop),
    ]
