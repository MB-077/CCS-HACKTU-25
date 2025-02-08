from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(required=False)
    
    class Meta:
        model = Account
        fields = ['id','first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}, 'phone_number': {'write_only': True}, 'id': {'read_only': True}, 'first_name': {'write_only': True}, 'last_name': {'write_only': True}}
        
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        if Account.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        
        if Account.objects.filter(phone_number=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'phone_number': 'Phone number already exists.'})
        
        account = Account(phone_number=self.validated_data['phone_number'], first_name=self.validated_data['first_name'], last_name=self.validated_data['last_name'], email=self.validated_data['email'])
        account.set_password(password)
        account.save()
        
        return account
    

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Phone Number or Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = None

            # Checking if username is an email or phone number
            if '@' in username:
                try:
                    user = Account.objects.get(email=username)
                except Account.DoesNotExist:
                    msg = _('No account found with this email.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                try:
                    user = Account.objects.get(phone_number=username)
                except Account.DoesNotExist:
                    msg = _('No account found with this phone number.')
                    raise serializers.ValidationError(msg, code='authorization')

            # Authenticating the user
            authenticated_user = authenticate(request=self.context.get('request'), username=username, password=password)

            if user and not authenticated_user:
                msg = _('Invalid password.')
                raise serializers.ValidationError(msg, code='authorization')

            if not authenticated_user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = authenticated_user
        return attrs
    

