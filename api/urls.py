from rest_framework.routers import DefaultRouter
from .views import MindMapViewSet, AppUserRegisterView, AppUserLoginView
from django.urls import path

router = DefaultRouter()
router.register(r'mindmaps', MindMapViewSet, basename='mindmap')

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
] + router.urls