from django import forms
from .models import RegisteredUser

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    repository_uri = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your repository URI'})
    )
    class Meta:
        model = RegisteredUser
        fields = ['repository_uri', 'email']
