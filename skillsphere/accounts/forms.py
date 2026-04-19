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


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        exclude = ('user',)


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        exclude = ('user',)
