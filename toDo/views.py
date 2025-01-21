from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from .forms import LoginForm, TaskForm, TeamForm, UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse
from django.db import IntegrityError

from .models import Task, Team

import logging

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
        # print("POST")
        form = LoginForm(request.POST)
        print("Form:", form)
        
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
            
            
            
            
        else:
            return render(
                request,
                "toDo/login.html",
                {"message":"The user is not found.", "form": form},
            )
    
    return render(request, "toDo/login.html", {"form": form})



def register(request):
    try:
        if request.user.id:
            return HttpResponseRedirect(reverse("dashboard"))

        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            print("Form submitted:", form)
            if form.is_valid():
                try:
                    form.save()
                except IntegrityError as e:
                    print("IntegrityError occurred:", e)
                    return render(request, "toDo/register.html", {"form": form, "message": "Username already exists."})
                form.save()
                return redirect("login")
            else:
                print("Form errors:", form.errors)
        else:
            form = UserRegisterForm()  # Initialize a blank form for GET requests
            print("Blank form initialized")

        return render(request, "toDo/register.html", {"form": form})
    except Exception as e:
        print("Error occurred:", e)  # Print the exact error to console
        return HttpResponseServerError("Server error")    

def logoutView(request):
    logout(request)
    return redirect("login")

def todosNew(request):
    team_id = 1  # Replace with actual logic to get team_id
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
    team_id = 1  # Replace with actual logic to get team_id
    
    try:
        task = get_object_or_404(Task, id=id)
        
        if request.method == "GET":
            form = TaskForm(instance=task)
            return render(request, "toDo/taskedit.html", {"form": form, "task": task, 'team_id': team_id})
        
        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
            else:
                return render(request, "toDo/taskedit.html", {"form": form, "task": task, 'team_id': team_id})
    
    except Task.DoesNotExist:
        return HttpResponseServerError("Task not found")
    except Exception as e:
        logger.exception("An error occurred while editing the task.")
        return HttpResponseServerError("Server error")

def teamsNew(request):
    team_id = 1  # Replace with actual logic to get team_id
    # return render(request, "toDo/createTeam.html")
    form = TeamForm(request.POST)
    if request.method == "POST":
        #form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TeamForm()
    # return render(request, "toDo/createTeam.html", {"form": form})
    return render(request, "toDo/createTeam.html", {"form": form, 'team_id': team_id})
    

def dashboard(request):
    try:
        # Get the first team (or return an error if no teams exist)
        team = Team.objects.first()
        if not team:
            logger.error("No teams found in the database.")
            return render(request, 'toDo/dashboard.html', {
                "message": 'No teams found. Please create a team first.', 'team_id': 0
            })

        team_id = team.id  # Access the ID of the first team
        teams = Team.objects.all()  # Get all teams

        # Get all tasks associated with the selected team
        todo_items = Task.objects.filter(user=request.user)
        print("Tasks:", todo_items)

        # Pass the data to the template
        context = {
            'team_id': team_id,
            'todo_items': todo_items,
            'teams': teams,
        }

        return render(request, 'toDo/dashboard.html', context)

    except Exception as e:
        # Print the error to the console and return a server error response
        logger.exception("An error occurred while accessing the dashboard.")
        print("Error occurred:", e)
        return HttpResponseServerError("Server error")




def teams(request, id):
    # todo_id = 1  # Replace with actual logic to get team_id
    # return render(request, "toDo/teamdetails.html", {'team_id': id, 'todo_id': todo_id})


    #list team name, description, and members
    team = Team.objects.get(id=id)
    print("Team:", team)
    team_id = team.id
    team_name = team.name
    team_description = team.description
    team_members = team.members.all()
    
    # Get all tasks associated with the selected team
    todo_items = Task.objects.filter(team=team)
    print("Tasks:", todo_items)
    
    # Pass the data to the template
    context = {
        'team_id': team_id,
        'team_name': team_name,
        'team_description': team_description,
        'team_members': team_members,
        'todo_items': todo_items,
    }
    
    return render(request, 'toDo/teamdetails.html', context)

    
    
def landing(request):
    return render(request, "toDo/landingpage.html")

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