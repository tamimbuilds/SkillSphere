from django.db import migrations, models
from django.db.models import Count


def merge_duplicate_candidate_skills(apps, schema_editor):
    CandidateSkill = apps.get_model('skills', 'CandidateSkill')
    Certificate = apps.get_model('skills', 'Certificate')
    Score = apps.get_model('skills', 'Score')
    Assessment = apps.get_model('skills', 'Assessment')

    duplicate_groups = (
        CandidateSkill.objects.values('candidate_id', 'skill_id')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )

    for group in duplicate_groups:
        candidate_skills = list(
            CandidateSkill.objects.filter(
                candidate_id=group['candidate_id'],
                skill_id=group['skill_id'],
            ).order_by('id')
        )
        keeper = candidate_skills[0]

        for duplicate in candidate_skills[1:]:
            Certificate.objects.filter(candidate_skill_id=duplicate.id).update(candidate_skill_id=keeper.id)
            Assessment.objects.filter(candidate_skill_id=duplicate.id).update(candidate_skill_id=keeper.id)

            for score in Score.objects.filter(candidate_skill_id=duplicate.id).iterator():
                score_conflict = Score.objects.filter(
                    user_id=score.user_id,
                    candidate_skill_id=keeper.id,
                    attempt_number=score.attempt_number,
                ).exists()
                if score_conflict:
                    Assessment.objects.filter(score_record_id=score.id).delete()
                    score.delete()
                else:
                    score.candidate_skill_id = keeper.id
                    score.save(update_fields=['candidate_skill'])

            duplicate.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0007_candidateskillprogress'),
    ]

    operations = [
        migrations.RunPython(merge_duplicate_candidate_skills, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='candidateskill',
            constraint=models.UniqueConstraint(fields=('candidate', 'skill'), name='unique_candidate_skill'),
        ),
    ]
