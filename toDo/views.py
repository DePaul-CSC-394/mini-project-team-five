from django.http import HttpResponseRedirect, HttpResponseServerError
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from toDoList import settings
from users.models import CustomUser
from .forms import LoginForm, PasswordResetForm, TaskForm, TeamForm, UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db import IntegrityError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import Task, Team

import json
import logging
from django.db.models import Q

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the toDo index.")
    context = {
        'key': 'value',  # Add any context data your template needs
    }
    return render(request, "toDo/landingpage.html", context)

def about(request):
    # return HttpResponse("About Page Test")
    
    return render(request, "toDo/about.html")

# class CustomLoginView(LoginView):
#     template_name = 'base/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True
    
#     def get_success_url(self):
#         return reverse_lazy('tasks')


    #https://stackoverflow.com/questions/77253258/django-function-based-view-login
def login(request):
    # print("login")
    # print("Request Method:", request.method)
    # print("User:", request.user)
    # print("POST Data:", request.POST)
       
    #redirect already login used
    if request.user.id:
        return HttpResponseRedirect(reverse("dashboard"))
    
    form = LoginForm(request.POST) #https://stackoverflow.com/questions/10023213/extracting-items-out-of-a-querydict
    if request.method == "POST":
    #     # print("POST")
    #     form = LoginForm(request.POST)
    #     print("Form:", form)
        
    #     if form.is_valid():
    #         email = form.cleaned_data.get("email")
    #         password = form.cleaned_data.get("password")
            
    #         login_user = authenticate(request, email=email, password=password)
    #         if login_user is not None:
    #             login_user.backend = 'users.authBackend.emailBackend.EmailBackend'
    #             auth_login(request, login_user)
    #             return redirect('/dashboard')
            
    #         else:
    #             return render(
    #                 request,
    #                 "toDo/login.html",
    #                 {"message":"The user is not found.", "form": form},
    #             )   
    # else:
    #     form = LoginForm()
    
    # context = {
    #     "form": form
    # }
    # return render(request, "toDo/login.html", context)
            
        
        if form:
            email = request.POST.get("email")
            password = request.POST.get("password")
            print("Email:", email)
            print("Password:", password)
            login_user = authenticate(request, email=email, password=password)
            if login_user is not None:
                login_user.backend = 'users.authBackend.emailBackend.EmailBackend'
                auth_login(request, login_user)
                return redirect('/dashboard')
            elif email not in CustomUser.objects.values_list('email', flat=True):
                return render(
                    request,
                    "toDo/login.html",
                    {"message":"The user is not found.", "form": form},
                )
            else:
                return render(
                    request,
                    "toDo/login.html",
                    {"message":"The password is incorrect.", "form": form},
                )
            
            # else:
            #     print("The user is not found.")
            #     return render(
            #         request,
            #         "toDo/login.html",
            #         {"message":"The user is not found.", "form": form},
            #     )
            
            
            
        else:
            return render(
                request,
                "toDo/login.html",
                {"message":"The user is not found.", "form": form},
            )
    
    return render(request, "toDo/login.html", {"form": form})
    



def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    # if request.user.id:
    #         return HttpResponseRedirect(reverse("dashboard"))
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        print("Form submitted:", form)
        if form.is_valid():
            try:
                form.save()
                # messages.success(request, "Registration successful. Please log in.")
                return redirect("login")
            except IntegrityError as e:
                print("IntegrityError occurred:", e)
                messages.error(request, "An error occurred: " + str(e))
                # return render(request, "toDo/register.html", {"form": form, "message": "Username already exists."})
            # form.save()
            # return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            print("Form errors:", form.errors)
    else:
        form = UserRegisterForm()  # Initialize a blank form for GET requests
        print("Blank form initialized")

    return render(request, "toDo/register.html", {"form": form})
    # except Exception as e:
    #     print("Error occurred:", e)  # Print the exact error to console
    #     return HttpResponseServerError("Server error")    

def logoutView(request):
    logout(request)
    return redirect("login")

def update_team(request, id):
    if request.method == "POST":
        team = get_object_or_404(Team, id=id)
        
        # Update description
        team.description = request.POST.get("description", team.description)
        
        # Handle new members
        new_members = request.POST.get("new_members", "[]")
        try:
            new_members = json.loads(new_members)
        except json.JSONDecodeError:
            new_members = []

        for email in new_members:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                if user in team.members.all():
                    messages.error(request, f"User {email} is already in the team")
                else:
                    team.members.add(user)
            else:
                messages.error(request, f"User {email} not found")


        # Handle removed members
        removed_members = request.POST.get("removed_members", "[]")
        try:
            removed_members = json.loads(removed_members)
        except json.JSONDecodeError:
            removed_members = []

        for email in removed_members:
            user = CustomUser.objects.filter(email=email).first()
            if user:
                team.members.remove(user)

        team.save()
        messages.success(request, "Team updated successfully")
        return redirect('teams', id=team.id)
    else:
        team = get_object_or_404(Team, id=id)
        form = TeamForm(instance=team)
        team_members = team.members.all()
        users_not_in_team = CustomUser.objects.exclude(teams=team)
        
        context = {
            'form': form,
            'team_id': team.id,
            'team_name': team.name,
            'team_description': team.description,
            'team_owner': team.owner,
            'team_members': team_members,
            'users_not_in_team': users_not_in_team,
        }
        
        return render(request, 'toDo/teamdetails.html', context)


def todosNew(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get the first team (or return an error if no teams exist)
    team = Team.objects.first()
    # if not team:
    #     logger.error("No teams found in the database.")
    #     return render(request, 'toDo/dashboard.html', {
    #         "message": 'No teams found. Please create a team first.', 'team_id': 0
    #     })

    team_id = team.id if team else 0  # Access the ID of the first team, or 0 if no team exists
    teams = Team.objects.all()  # Get all teams
    # return render(request, "toDo/createToDo.html", {'team_id': team_id})
    
    if request.method == "POST":
        form = TaskForm(request.POST)
        print("Form:", form)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            print("Form saved")
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, "toDo/createToDo.html", {"form": form,'team_id': team_id})


def todosEdit(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # team = Team.objects.first()
    # team_id = team.id if team else 0 

    try:
        task = get_object_or_404(Task, id=id)
        team = task.team
        team_id = team.id if team else 0 
        
        if request.method == "GET":
            form = TaskForm(instance=task)
            return render(request, "toDo/createToDo.html", {"form": form, "task": task, 'team_id': team_id})
        
        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
            else:
                return render(request, "toDo/createToDo.html", {"form": form, "task": task, 'team_id': team_id})
    
    except Task.DoesNotExist:
        return HttpResponseServerError("Task not found")
    except Exception as e:
        logger.exception("An error occurred while editing the task.")
        return HttpResponseServerError("Server error")

def teamsNew(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    team = Team.objects.first()
    team_id = team.id if team else 0 
    # return render(request, "toDo/createTeam.html")
    
    #form = TeamForm(request.POST)
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user
            team.save()
            
            return redirect('dashboard')
            # form.save()
            # return redirect('dashboard')
    else:
        form = TeamForm()
    # return render(request, "toDo/createTeam.html", {"form": form})
    return render(request, "toDo/createTeam.html", {"form": form, 'team_id': team_id})
    

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        # Get the first team (or return an error if no teams exist)
        team = Team.objects.first() #get l
        # if not team:
        #     logger.error("No teams found in the database.")
        #     return render(request, 'toDo/dashboard.html', {
        #         "message": 'No teams found. Please create a team first.', 'team_id': 0
        #     })

        team_id = team.id if team else 0  # Access the ID of the first team, or 0 if no team exists
        teams = Team.objects.all()  # Get all teams

        # Get all tasks associated with the selected team
        todo_items = Task.objects.filter(user=request.user)
        # commented out because we want team filtering to occur with dropdown box
        # todo_items = todo_items | Task.objects.filter(team=team) # | is the union operator
        categories = todo_items.values_list('category', flat=True).distinct()

        print("Tasks:", todo_items)

        # Pass the data to the template
        context = {
            'team_id': team_id,
            'todo_items': todo_items,
            'categories': categories,
            'teams': teams,
            'team_name': team.name if team else None,
        }

        return render(request, 'toDo/dashboard.html', context)

    except Exception as e:
        # Print the error to the console and return a server error response
        logger.exception("An error occurred while accessing the dashboard.")
        print("Error occurred:", e)
        return HttpResponseServerError("Server error")

def teams(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user_teams_ids = Team.objects.filter(members=request.user).values_list('id', flat=True) | Team.objects.filter(owner=request.user).values_list('id', flat=True)
    # if id not in user_teams_ids:
    #     return redirect('teams_new')
    
    if id == 0: 
        return redirect('teams_new')

    team = get_object_or_404(Team, id=id)
    team_members = team.members.all()
    todo_items = Task.objects.filter(team=team)
    users_not_in_team = CustomUser.objects.filter(~Q(teammember__team=team))
    user_teams = Team.objects.filter(members=request.user) | Team.objects.filter(owner=request.user) #can be member or owner

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('teams', id=team.id)
    else:
        form = TeamForm(instance=team)

    context = {
        'form': form,
        'team_id': team.id,
        'team_name': team.name,
        'team_description': team.description,
        'team_owner': team.owner,
        'team_members': team_members,
        'todo_items': todo_items,
        'users_not_in_team': users_not_in_team,
        'user_teams': user_teams,
    }

    return render(request, 'toDo/teamdetails.html', context)

    
    
def landing(request):
    return render(request, "toDo/landingpage.html")

def delete(request, id):
    task = Task.objects.get(id=id) # Get the task object
    task.delete() # Delete the task
    return redirect('dashboard')

# def task(request):
#     return render(request, "toDo/task.html")

# def LoginView(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
        
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect("/")
#         else:
#             return render(request, "toDo/login.html", {"message": "Invalid credentials"})
# def update_team(request, id):



def delete_team(request, id):
    if not request.user.is_authenticated:
        return redirect('login')

    team = get_object_or_404(Team, id=id)

    if request.method == 'GET' or request.method == 'POST':
        team.delete()
        return redirect('dashboard')
    return redirect('dashboard')

def forgot_password(request):
    form = PasswordResetForm()
    if request.method == "POST":
        email = request.POST.get("email")
        # if not CustomUser.objects.filter(email=email).exists():
        #     messages.error(request, "Email not found.")
        try:
            user = CustomUser.objects.get(email=email)
            if user:
                #generate token and uid
                token = PasswordResetTokenGenerator().make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                resetLink = request.build_absolute_uri(reverse('reset_password', kwargs={'uidb64': uid, 'token': token})).replace(request.get_host(), f"{request.get_host().split(':')[0]}:1337")
                
                
                #send email
                send_mail(
                    'Password Reset',
                    f'Click the link to reset your password: {resetLink}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                # Add code to send password reset email
                messages.success(request, "Password reset email sent.")
                return render(request, "toDo/forgotpsw.html", {"form": form})
        except CustomUser.DoesNotExist:
            return render(request, "toDo/forgotpsw.html", {"message": "Email not found", "form": form})
    return render(request, "toDo/forgotpsw.html", {"form": form})


def reset_password(request, uidb64, token):
    # return render(request, "toDo/recoverPassword.html")

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(CustomUser, pk=uid)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            return render(request, "toDo/recoverPassword.html", {"message": "Invalid or expired token"})
        
        if request.method == "POST":
            newPassword = request.POST.get("password")
            confirmPassword = request.POST.get("confirm-password")
            
            if newPassword != confirmPassword:
                return render(request, "toDo/recoverPassword.html", {"message": "Passwords do not match"})
            
            user.set_password(newPassword)
            user.save()
            
            return redirect('login')
        return render(request, "toDo/recoverPassword.html")
    except Exception as e:
        print("Error occurred:", e)
        return render(request, "toDo/recoverPassword.html", {"message": "Error occurred"})
        
def addMember(request, id):
    team = get_object_or_404(Team, id=id)
    
    if request.method == "POST":
        new_member_id = request.POST.get("email")
        
        if not new_member_id:
            messages.error(request, "Member not found")
            return redirect('teams', id=id)
        try:
            new_member = get_object_or_404(CustomUser, email=new_member_id)
            
            #check if member is already in the team
            if new_member in team.members.all():
                messages.error(request, "Member already in team")
                return redirect('teams', id=id)
            else:
                team.members.add(new_member)
                return redirect('teams', id=id)
            
        except CustomUser.DoesNotExist:
            messages.error(request, "Member not found")
            return redirect('teams', id=id)
        
        except Exception as e:
            messages.error(request, f"Error occurred: {e}")
            return redirect('teams', id=id)
        
            
        return redirect('teams', id=id)

    return redirect('teams', id=id)

@csrf_exempt
def update_task_state(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            data = json.loads(request.body)
            state = data.get('state')
            secondsElapsed = data.get('secondsElapsed', 0)
            if state == 'running':
                task.timer.isRunning = True
                task.timer.isPaused = False
            elif state == 'paused':
                task.timer.isRunning = False
                task.timer.isPaused = True
            elif state == 'stopped':
                task.timer.isRunning = False
                task.timer.isPaused = False
                task.timer.secondsElapsed = 0
            task.timer.secondsElapsed = secondsElapsed
            task.timer.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def fetch_timers(request):
    tasks = Task.objects.all()
    timers = []
    for task in tasks:
        timers.append({
            'taskId': task.id,
            'secondsElapsed': task.timer.secondsElapsed,
            'isRunning': task.timer.isRunning,
        })
    return JsonResponse({'timers': timers})