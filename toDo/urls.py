from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="landingpageunauth"),
    path("about/", views.about, name="about"),
    path("login/", views.login, name = "login"),
    path("todos/new", views.todosNew, name = "todocreate"),
    path("teams/new", views.teamsNew, name = "teamcreate"),
    path("dashboard/", views.dashboard, name = "emptydashboard"),
]