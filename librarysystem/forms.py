
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',  # Remove the label
        widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='',  # Remove the label
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )