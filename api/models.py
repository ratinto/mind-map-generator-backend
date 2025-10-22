from django.db import models
from django.utils import timezone

class AppUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 

    def __str__(self):
        return self.username

class MindMap(models.Model):
    name = models.CharField(max_length=100)
    nodes = models.JSONField(default=list) 
    edges = models.JSONField(default=list)
    drawing_paths = models.JSONField(default=list)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='mindmaps', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username if self.owner else 'No Owner'}"
    

