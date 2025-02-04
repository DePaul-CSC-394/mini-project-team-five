import datetime
from django import forms 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from users.models import CustomUser
from django.contrib.auth import authenticate
from django.db import models

from .models import Task, Team


class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name':'password'}))
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            if not CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("Invalid email or password")
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password")
            
        return cleaned_data
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
    
        
#https://www.devhandbook.com/django/user-registration/
#https://www.crunchydata.com/blog/building-a-user-registration-form-with-djangos-built-in-authentication
class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    #password1 = forms.CharField(widget=forms.PasswordInput(attrs={'name':'password'}))
    #password2 = forms.CharField(widget=forms.PasswordInput(attrs={'name':'confirm'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'name': 'email',
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        if commit:
            user.save()
        return user
    
#https://docs.djangoproject.com/en/5.1/topics/forms/    
class TaskForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'name':'title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'description'}))
    dueDate = forms.DateField(widget=forms.DateInput(attrs={'name':'dueDate', 'type': 'date'}), required=False)
    category = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'name':'category'}), required=False)
    team = forms.ModelChoiceField(queryset=Team.objects.all(), widget=forms.Select(attrs={'name':'team'}), required=False)
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.Select(attrs={'name':'assignee'}), required=False)

    def clean_dueDate(self):
        dueDate = self.cleaned_data.get('dueDate')
        if dueDate and dueDate < datetime.date.today():
            raise forms.ValidationError("The due date must be in the future.")
        return dueDate

    class Meta:
        model = Task
        fields = ['title', 'description', 'dueDate', 'category', 'team']

    def init(self, args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskForm, self).init(args, **kwargs)
        if self.user:
            self.fields['team'].queryset = Team.objects.filter(members=self.user)
            self.fields['user'].initial = self.user

        
class TeamForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'name':'name'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'name':'description'}))
    #members = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.all(), widget=forms.SelectMultiple(attrs={'name':'members'}), required=False)
    
    class Meta:
        model = Team
        fields = ['name', 'description']
        #fields = ['name', 'description', 'members'] # need to add members to fields
        
    

class PasswordResetForm(forms.Form): #form for forgot password page
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name':'email'}))
    
class AddMemeberForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User does not exist.")
        return email

    
    
    
    