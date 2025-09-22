from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import MindMap, AppUser
from .serializers import MindMapSerializer, AppUserRegisterSerializer, AppUserLoginSerializer, AppUserSerializer
from django.contrib.auth.hashers import make_password, check_password

class MindMapViewSet(viewsets.ModelViewSet):
    serializer_class = MindMapSerializer
    
    def get_queryset(self):
        # Get user_id from request (stored in session or passed as parameter)
        user_id = self.request.session.get('user_id') or self.request.GET.get('user_id')
        if user_id:
            try:
                app_user = AppUser.objects.get(id=user_id)
                return MindMap.objects.filter(owner=app_user)
            except AppUser.DoesNotExist:
                return MindMap.objects.none()
        return MindMap.objects.none()
    
    def perform_create(self, serializer):
        # Get user_id from request
        user_id = self.request.session.get('user_id') or self.request.data.get('user_id')
        if user_id:
            try:
                app_user = AppUser.objects.get(id=user_id)
                serializer.save(owner=app_user)
            except AppUser.DoesNotExist:
                raise serializers.ValidationError("Invalid user")
        else:
            serializer.save()  # Save without owner for now

class AppUserRegisterView(APIView):
    def post(self, request):
        serializer = AppUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create AppUser with hashed password
                app_user = AppUser.objects.create(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=make_password(serializer.validated_data['password'])
                )
                
                return Response({
                    'message': 'User registered successfully',
                    'user_id': app_user.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': f'Registration failed: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppUserLoginView(APIView):
    def post(self, request):
        serializer = AppUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                app_user = AppUser.objects.get(username=username)
                if check_password(password, app_user.password):
                    # Store user_id in session
                    request.session['user_id'] = app_user.id
                    
                    return Response({
                        'message': 'Login successful',
                        'user_id': app_user.id,
                        'username': app_user.username,
                        'access_token': f'user_{app_user.id}',  # Simple token for now
                        'refresh_token': f'refresh_user_{app_user.id}'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except AppUser.DoesNotExist:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_profile(request):
    """Get current user profile"""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            app_user = AppUser.objects.get(id=user_id)
            serializer = AppUserSerializer(app_user)
            return Response(serializer.data)
        except AppUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)