from django import forms 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from users.models import CustomUser
from django.db import models

from .models import Task, Team


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
    
#https://docs.djangoproject.com/en/5.1/topics/forms/    
class TaskForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'name':'title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'description'}))
    dueDate = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'name':'dueDate'}), required=False)
    category = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'name':'category'}), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.Select(attrs={'name':'team'}), required=False)
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'dueDate', 'category', 'team']
        
class TeamForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'name':'name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'description'}), required=False)
    members = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), widget=forms.SelectMultiple(attrs={'name':'members'}), required=False)
    
    class Meta:
        model = Team
        fields = ['name', 'description', 'members']
    