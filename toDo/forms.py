from django import forms 
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email here'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password here'}))
    
    class Meta:
        fields = ['email']
        
        