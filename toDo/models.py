from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

from users.models import CustomUser   

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    members = models.ForeignKey(CustomUser, on_delete= models.CASCADE, default=None)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class stopwatch(models.Model):
    startTime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)
    isRunning = models.BooleanField(default=False)
    
    def start(self):
        self.startTime = timezone.now()
        self.isRunning = True
        self.save()
        
    def stop(self):
        self.endTime = timezone.now()
        self.isRunning = False
        self.save()
        
    def timeElasped(self):
        if self.isRunning:
            return timezone.now() - self.startTime
        elif self.endTime:
            return self.endTime - self.startTime
        else:
            return None
        
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # on_delete=models.CASCADE means that if the user is deleted, all the tasks associated with that user will also be deleted
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    dueDate= models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete= models.CASCADE, default= None, null=True)
    
    
    
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']  # ordering within the database
        
