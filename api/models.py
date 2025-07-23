from django.db import models

class MindMap(models.Model):
    name = models.CharField(max_length=100)
    nodes = models.JSONField(default=list)  # Store nodes as JSON, default empty list
    edges = models.JSONField(default=list)  # Store edges as JSON, default empty list

    def __str__(self):
        return self.name