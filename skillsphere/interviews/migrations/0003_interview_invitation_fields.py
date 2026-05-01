from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='interview_type',
            field=models.CharField(choices=[('technical', 'Technical'), ('hr', 'HR'), ('final', 'Final')], default='hr', max_length=20),
        ),
        migrations.AlterField(
            model_name='interview',
            name='interviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interviews.interviewer'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='round_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='interview',
            name='contact_details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='interview',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interview',
            name='welcome_message',
            field=models.TextField(blank=True),
        ),
    ]
