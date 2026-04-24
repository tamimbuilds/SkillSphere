from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, CandidateProfile, RecruiterProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phone', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    pass


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'profile_image']


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'specialized_sector', 'university', 'department', 'cgpa', 'graduation_year', 'bio', 'linkedin_url', 'github_url', 'portfolio_url']


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        exclude = ('user',)
