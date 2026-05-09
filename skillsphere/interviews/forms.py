from django import forms
from .models import Interview, Interviewer, Shortlist


class InterviewerForm(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = ['full_name', 'email', 'designation', 'department', 'phone']


class ShortlistForm(forms.ModelForm):
    class Meta:
        model = Shortlist
        fields = '__all__'


class InterviewForm(forms.ModelForm):
    scheduled_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    scheduled_time = forms.TimeField(
        input_formats=['%H:%M', '%H:%M:%S'],
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'step': '60'})
    )

    class Meta:
        model = Interview
        fields = '__all__'
        widgets = {
            'welcome_message': forms.Textarea(attrs={'rows': 4}),
            'feedback': forms.Textarea(attrs={'rows': 4}),
            'contact_details': forms.Textarea(attrs={'rows': 3}),
        }


class RecruiterInterviewInviteForm(forms.ModelForm):
    scheduled_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    scheduled_time = forms.TimeField(
        input_formats=['%H:%M', '%H:%M:%S'],
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'step': '60'})
    )

    class Meta:
        model = Interview
        fields = ['welcome_message', 'scheduled_date', 'scheduled_time', 'location', 'contact_details', 'meeting_link']
        labels = {
            'welcome_message': 'Welcome message',
            'scheduled_date': 'Interview date',
            'scheduled_time': 'Interview time',
            'location': 'Venue',
            'contact_details': 'Contact details',
            'meeting_link': 'Meeting link',
        }
        widgets = {
            'welcome_message': forms.Textarea(attrs={'rows': 5}),
            'location': forms.TextInput(attrs={'placeholder': 'Office address or online venue'}),
            'contact_details': forms.Textarea(attrs={'rows': 4}),
            'meeting_link': forms.URLInput(attrs={'placeholder': 'https://meet.example.com/...'}),
        }
