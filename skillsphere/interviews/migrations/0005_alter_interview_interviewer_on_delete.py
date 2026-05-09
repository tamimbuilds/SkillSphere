import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0004_alter_interview_scheduled_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='interviewer',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='interviews.interviewer',
            ),
        ),
    ]
