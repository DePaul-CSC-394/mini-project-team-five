from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    # path("task/<int:pk>/", views.todosNew, name = "task"),
    path("register/", views.register, name = "register"),
    path("login/", views.login, name = "login"),
    path("dashboard/", views.dashboard, name = "dashboard"),
    path("teams/new", views.teamsNew, name = "teams_new"),
    path("todos/new", views.todosNew, name = "createToDo"),
    path("todos/<int:id>/edit", views.todosEdit, name = "todos_edit"),
    path('teams/<int:id>/', views.teams, name='teamList'),
    path("landing/", views.landing, name = "landing"),
    path("logout/", views.logoutView, name = "logout"),
]