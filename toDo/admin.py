from django.contrib import admin


from .models import Task, Team, stopwatch
#from django.contrib.auth.models import UserAdmin
#from users.models import CustomUser

# Register your models here.

admin.site.register(Task)
admin.site.register(Team)
admin.site.register(stopwatch)

#admin.site.register(CustomUser)

