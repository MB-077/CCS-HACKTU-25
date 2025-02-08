from django.urls import path, include
from django.urls import re_path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='userprofile')
router.register(r'important-details', views.UserImportantDetailsViewSet, basename='importantdetails')

urlpatterns = [
    path('register/', views.registration_view, name='register'),  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgotPassword, name='forgot_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('resetpassword_validate/<str:uidb64>/<str:token>/', views.resetpassword_validate, name='resetpassword_validate'),
    re_path(r'^resetpassword_validate/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/?$', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('', include(router.urls)),
]

