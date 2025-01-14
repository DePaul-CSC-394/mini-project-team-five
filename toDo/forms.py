from django import forms 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name':'password'}))
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
        