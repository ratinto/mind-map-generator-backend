from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MindMap, AppUser
from .serializers import MindMapSerializer, AppUserRegisterSerializer, AppUserLoginSerializer
from django.contrib.auth.hashers import make_password, check_password

class MindMapViewSet(viewsets.ModelViewSet):
    queryset = MindMap.objects.all()
    serializer_class = MindMapSerializer

class AppUserRegisterView(APIView):
    def post(self, request):
        serializer = AppUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the password before saving
            serializer.save(password=make_password(serializer.validated_data['password']))
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppUserLoginView(APIView):
    def post(self, request):
        serializer = AppUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = AppUser.objects.get(username=serializer.validated_data['username'])
                if check_password(serializer.validated_data['password'], user.password):
                    return Response({'message': 'Login successful', 'user_id': user.id})
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except AppUser.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)