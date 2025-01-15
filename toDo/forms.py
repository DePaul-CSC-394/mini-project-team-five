from django import forms 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from users.models import CustomUser


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name':'password'}))
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        
#https://www.devhandbook.com/django/user-registration/
#https://www.crunchydata.com/blog/building-a-user-registration-form-with-djangos-built-in-authentication
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    #password1 = forms.CharField(widget=forms.PasswordInput(attrs={'name':'password'}))
    #password2 = forms.CharField(widget=forms.PasswordInput(attrs={'name':'confirm'}))
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
    
    