from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import LoginForm
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse

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

def todosNew(request):
    return render(request, "toDo/createToDo.html")

def teamsNew(request):
    return render(request, "toDo/createTeam.html")

def dashboard(request):
    team_id = 1  # Replace with actual logic to get team_id
    return render(request, 'toDo/dashboard.html', {'team_id': team_id})

def register(request):
    return render(request, "toDo/register.html")

def todosEdit(request):
    return render(request, "toDo/createToDo.html")

def teams(request):
    return render(request, "toDo/teamdetails.html", {'team_id': id})

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