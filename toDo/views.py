from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import redirect, render
from .forms import LoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse
from django.db import IntegrityError


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
                return redirect('dashboard')
            
            
            
            
        else:
            return render(
                request,
                "toDo/login.html",
                {"message":"The user is not found.", "form": form},
            )
    
    return render(request, "toDo/login.html", {"form": form})


# def register(request):
#     #redirect already login used
#     if request.user.id:
#         return HttpResponseRedirect(reverse("dashboard"))
    
#     #form = UserRegisterForm(request.POST)
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#         else:
#             form = UserRegisterForm()
#         return render(request, "toDo/register.html", {"form": form})
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
        
        
        
        
                      
        
        # if form.is_valid():
        #     print("Form is valid")
        #     email = form.cleaned_data.get("email")
        #     password = form.cleaned_data.get("password")
        #     user = authenticate(request, email=email, password=password)
        #     if user is not None:
        #         auth_login(request, user)
        #         return HttpResponseRedirect("dashboard")
                
    #     else:
    #         return render(
    #             request,
    #             "toDo/login.html",
    #             {"message":"The user is not found.", "form": form},
    #         )
    # else :
    #     form = LoginForm()
    
    # return render(request, "toDo/login.html", {"form": form})

def logoutView(request):
    logout(request)
    return redirect("login")

def todosNew(request):
    team_id = 1  # Replace with actual logic to get team_id
    return render(request, "toDo/createToDo.html", {'team_id': team_id})

def teamsNew(request):
    return render(request, "toDo/createTeam.html")

def dashboard(request):
    team_id = 1  # Replace with actual logic to get team_id
    todo_id = 1  # Replace with actual logic to get todo_id
    return render(request, 'toDo/dashboard.html', {'team_id': team_id, 'todo_id': todo_id})


def todosEdit(request, id):
    team_id = 1  # Replace with actual logic to get team_id
    return render(request, "toDo/createToDo.html", {'todo_id': id, 'team_id': team_id})

def teams(request, id):
    todo_id = 1  # Replace with actual logic to get team_id
    return render(request, "toDo/teamdetails.html", {'team_id': id, 'todo_id': todo_id})

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