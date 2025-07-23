from django.db import models

class MindMap(models.Model):
    name = models.CharField(max_length=100)
    nodes = models.JSONField(default=list) 
    edges = models.JSONField(default=list)

    def __str__(self):
        return self.name

class AppUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.username