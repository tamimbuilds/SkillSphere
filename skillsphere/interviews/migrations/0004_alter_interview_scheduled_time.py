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
    if schema_editor.connection.vendor == "postgresql":
        normalize_scheduled_times_postgres(schema_editor)
        return

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


def normalize_scheduled_times_postgres(schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE interviews_interview
            SET scheduled_time = CASE
                WHEN scheduled_time IS NULL OR btrim(scheduled_time) = '' THEN '09:00:00'
                WHEN btrim(scheduled_time) ~ '^[0-9]{1,2}:[0-9]{2}:[0-9]{2}$'
                    THEN to_char(btrim(scheduled_time)::time, 'HH24:MI:SS')
                WHEN btrim(scheduled_time) ~ '^[0-9]{1,2}:[0-9]{2}$'
                    THEN to_char(btrim(scheduled_time)::time, 'HH24:MI:SS')
                WHEN upper(btrim(scheduled_time)) ~ '^[0-9]{1,2}:[0-9]{2}:[0-9]{2} (AM|PM)$'
                    THEN to_char(to_timestamp(upper(btrim(scheduled_time)), 'HH12:MI:SS AM')::time, 'HH24:MI:SS')
                WHEN upper(btrim(scheduled_time)) ~ '^[0-9]{1,2}:[0-9]{2} (AM|PM)$'
                    THEN to_char(to_timestamp(upper(btrim(scheduled_time)), 'HH12:MI AM')::time, 'HH24:MI:SS')
                WHEN upper(btrim(scheduled_time)) ~ '^[0-9]{1,2} (AM|PM)$'
                    THEN to_char(to_timestamp(upper(btrim(scheduled_time)), 'HH12 AM')::time, 'HH24:MI:SS')
                ELSE '09:00:00'
            END
            """
        )


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
