from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0003_interview_invitation_fields'),
        ('accounts', '0003_alter_candidateprofile_specialized_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='interview',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications', to='interviews.interview'),
        ),
    ]
