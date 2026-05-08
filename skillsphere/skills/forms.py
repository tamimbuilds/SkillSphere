from django import forms
from .models import Skill, CandidateSkill, Certificate, JobSkillRequirement


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'category', 'description']


class CandidateSkillForm(forms.ModelForm):
    proficiency_level = forms.ChoiceField(
        choices=CandidateSkill.PROFICIENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    years_of_experience = forms.ChoiceField(
        choices=CandidateSkill.EXPERIENCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        sector = kwargs.pop('sector', None)
        super().__init__(*args, **kwargs)
        if sector:
            # Assuming Skill category matches CandidateProfile specialized_sector
            self.fields['skill'].queryset = Skill.objects.filter(category__icontains=sector)

    class Meta:
        model = CandidateSkill
        fields = ['skill', 'proficiency_level', 'years_of_experience']


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = '__all__'

class CandidateCertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'certificate_file', 'issued_by', 'issue_date', 'expiry_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. AWS Certified Solutions Architect'}),
            'issued_by': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Amazon Web Services'}),
        }

class JobSkillRequirementForm(forms.ModelForm):
    class Meta:
        model = JobSkillRequirement
        fields = ['job', 'skill', 'required_level', 'is_mandatory']

