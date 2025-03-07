from django.shortcuts import render

# Create your views here.

# Rest Framework imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework import viewsets
from .serializers import UserProfileSerializer, UserImportantDetailsSerializer

# General imports
from .serializers import *
from django.contrib.auth.models import User
from django.db import transaction 

# Email imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, BadHeaderError

# Debugging imports
import logging
logger = logging.getLogger(__name__)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        try:
            print(request.data)
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            TokenUsageLog.objects.create(
                token=token,
                user=user,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                path=request.path,
            )
            
            data = {
                'token': token.key,
                'registration_id': user.pk,
                'phone_number': user.phone_number,
                'full_name': user.full_name(),
                'email': user.email,
            }

            if hasattr(user, 'profile'):
                profile = user.profile
                profile_data = {
                    'user_profile_id': profile.id,
                    'latitude': profile.latitude,
                    'longitude': profile.longitude,
                    'land_area': profile.land_area,
                }
                data.update(profile_data)
                
            response = Response(data, status=status.HTTP_200_OK)
            return self.remember_me(request, response)

        except serializers.ValidationError as e:
            error_message = list(e.detail.values())[0][0] if e.detail else 'Validation error'
            return Response({'error serializer': error_message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def remember_me(self, request, response):
        remember_me = request.data.get('remember_me')
        if remember_me:
            response.set_cookie('phone_number', request.data.get('phone_number'), max_age=604800)
            response.set_cookie('password', request.data.get('password'), max_age=604800)
        else:
            response.delete_cookie('phone_number')
            response.delete_cookie('password')
        return response
        
        
@api_view(['POST'])
def logout_view(request):
    try:
        with transaction.atomic():
            if request.user.is_authenticated:
                request.user.auth_token.delete()
                return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        try:
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'Registration Successful!'
                data['registration_id'] = account.id
                data['first_name'] = account.first_name
                data['last_name'] = account.last_name
                data['phone_number'] = account.phone_number
                data['email'] = account.email
                
                token = Token.objects.get(user=account).key
                data['token'] = token

                return Response(data, status=status.HTTP_201_CREATED)
            else:
                error_message = list(serializer.errors.values())[0][0] if serializer.errors else 'Validation error'
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as e:
            error_message = list(e.detail.values())[0][0] if e.detail else 'Validation error'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST','PUT', 'GET'])
def change_password(request):
    if request.method == 'PUT':
        user = request.user
        current_password = request.data['current_password']
        new_password = request.data['new_password']
        new_password_confirm = request.data['new_password_confirm']
        
        if new_password != new_password_confirm:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(current_password):
            user.set_password(new_password_confirm)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def userprofile_view(request):
    if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        data = {}

        try:
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'Registration Successful!'
                data['registration_id'] = account.id
                data['first_name'] = account.first_name
                data['last_name'] = account.last_name
                data['phone_number'] = account.phone_number
                data['email'] = account.email
                
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                error_message = list(serializer.errors.values())[0][0] if serializer.errors else 'Validation error'
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as e:
            error_message = list(e.detail.values())[0][0] if e.detail else 'Validation error'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def forgotPassword(request):
    if request.method == "POST":
        email = request.data.get('email')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('Users/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            try:
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                return Response({'message': 'Password reset email has been sent to your email address.'}, status=status.HTTP_200_OK)
            except BadHeaderError:
                return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Account does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    return Response({'message': 'Forgot Password Complete'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def resetpassword_validate(request, uidb64, token):
    logger.debug(f"Received request: {request.method} {request.path}")
    logger.debug(f"UID: {uidb64}, Token: {token}")

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        logger.debug(f"Decoded UID: {uid}")
        user = User.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            return Response({'message': 'Valid link', 'uid': uid, 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Link has expired or is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        logger.error(f"Exception occurred: {str(e)}")
        return Response({'error': 'User not found or invalid UID'}, status=status.HTTP_404_NOT_FOUND)
        
    
@api_view(['POST'])   
def reset_password(request):
    if request.method == "POST":
        data = request.data 
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        uid = data.get('uid')

        if password and confirm_password:
            if password == confirm_password:
                if uid:
                    try:
                        user = User.objects.get(pk=uid)
                        user.set_password(password)
                        user.save()
                        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
                    except User.DoesNotExist:
                        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'error': 'Session expired'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Password and confirm password are required'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserImportantDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserImportantDetails.objects.all()
    serializer_class = UserImportantDetailsSerializer