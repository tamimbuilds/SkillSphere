from django import forms
from jobs.models import JobPost, Application, HiringInvitation, JobOffer

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title','description','required_cgpa','required_experience',
                  'salary_range','location','deadline','status']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }

class HiringInvitationForm(forms.ModelForm):
    class Meta:
        model = HiringInvitation
        fields = ['candidate', 'job', 'message']

class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ['offered_salary', 'joining_date', 'offer_letter']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }