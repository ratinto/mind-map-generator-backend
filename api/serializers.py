from rest_framework import serializers
from .models import MindMap, AppUser

class MindMapSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = MindMap
        fields = ['id', 'name', 'nodes', 'edges', 'drawing_paths', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

class AppUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class AppUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email']


