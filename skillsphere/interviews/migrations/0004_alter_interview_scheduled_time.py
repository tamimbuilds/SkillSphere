from django.db import migrations, models
from datetime import datetime


TIME_FORMATS = [
    "%H:%M:%S",
    "%H:%M",
    "%I:%M:%S %p",
    "%I:%M %p",
    "%I %p",
]


def normalize_scheduled_times(apps, schema_editor):
    Interview = apps.get_model("interviews", "Interview")

    for interview in Interview.objects.all().only("pk", "scheduled_time"):
        raw_time = (interview.scheduled_time or "").strip()
        normalized_time = None

        for time_format in TIME_FORMATS:
            try:
                normalized_time = datetime.strptime(raw_time.upper(), time_format).time()
                break
            except ValueError:
                continue

        if normalized_time is None:
            normalized_time = datetime.strptime("09:00", "%H:%M").time()

        interview.scheduled_time = normalized_time.strftime("%H:%M:%S")
        interview.save(update_fields=["scheduled_time"])


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_interview_invitation_fields'),
    ]

    operations = [
        migrations.RunPython(normalize_scheduled_times, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='interview',
            name='scheduled_time',
            field=models.TimeField(),
        ),
    ]
