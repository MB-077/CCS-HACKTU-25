from django.urls import path, include
from django.urls import re_path
from . import views
from django.shortcuts import render
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='userprofile')
router.register(r'important-details', views.UserImportantDetailsViewSet, basename='importantdetails')

urlpatterns = [
    path('register/', views.registration_view, name='register'),  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('', include(router.urls)),
]

