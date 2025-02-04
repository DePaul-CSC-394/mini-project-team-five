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
    path("todos/new", views.todosNew, name = "todos_new"),
    path("todos/<int:id>/edit", views.todosEdit, name = "todos_edit"),
    path('teams/<int:id>/', views.teams, name='teams'),
    path("landing/", views.landing, name = "landing"),
    path("logout/", views.logoutView, name = "logout"),
    path("delete/<int:id>/", views.delete, name = "delete"),
    path('teams/<int:id>/delete/', views.delete_team, name='delete_team'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('teams/<int:id>/add-member', views.addMember, name='add_member'),
    path('update_task_state/<int:task_id>/', views.update_task_state, name='update_task_state'),
    path('fetch_timers/', views.fetch_timers, name='fetch_timers'),
]
