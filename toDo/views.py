from django.shortcuts import render, HttpResponse, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the toDo index.")
    context = {
        'key': 'value',  # Add any context data your template needs
    }
    return render(request, "toDo/index.html", context)

def about(request):
    # return HttpResponse("About Page Test")
    
    return render(request, "toDo/about.html")


def login(request):#https://stackoverflow.com/questions/77253258/django-function-based-view-login
       
    #redirect already login used
    if request.user.id:
        return redirect("/")
    
    form = LoginForm()
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(user=username, password=password)
            login(request, user)
            return redirect("/")
        else:
            return render(
                request,
                "toDo/login.html",
                {"message":"The user is not found.", "form": form},
            )
    
    return render(request, "toDo/login.html")
    