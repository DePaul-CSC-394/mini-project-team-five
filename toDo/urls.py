from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="landingpageunauth"),
    path("about/", views.about, name="about"),

    path("todos/new", views.todosNew, name = "todocreate"),
    path("teams/new", views.teamsNew, name = "teamcreate"),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("register/", views.register, name = "register"),
    path("createToDo/", views.createToDo, name = "createToDo"),
    path("teamList/", views.teamList, name = "teamList"),
]