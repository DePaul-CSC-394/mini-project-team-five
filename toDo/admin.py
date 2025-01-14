from django.contrib import admin

from .models import Task, Team, stopwatch

# Register your models here.

admin.site.register(Task)
admin.site.register(Team)
admin.site.register(stopwatch)


