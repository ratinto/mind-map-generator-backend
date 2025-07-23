from rest_framework import serializers
from .models import MindMap, AppUser

class MindMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindMap
        fields = ['id', 'name', 'nodes', 'edges']

class AppUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class AppUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


