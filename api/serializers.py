from rest_framework import serializers
from .models import MindMap

class MindMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindMap
        fields = ['id', 'name', 'nodes', 'edges']


