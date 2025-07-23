from rest_framework import viewsets
from .models import MindMap
from .serializers import MindMapSerializer

class MindMapViewSet(viewsets.ModelViewSet):
    queryset = MindMap.objects.all()
    serializer_class = MindMapSerializer