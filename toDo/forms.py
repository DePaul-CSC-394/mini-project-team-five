from django import forms 
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name':'password'}))
    
    class Meta:
        fields = ['email']
        
        