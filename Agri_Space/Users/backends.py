from django.contrib.auth.backends import ModelBackend
from .models import Account

class PhoneNumberOrEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('phone_number') or kwargs.get('email')
        
        try:
            if '@' in username:
                user = Account.objects.get(email=username)
            else:
                user = Account.objects.get(phone_number=username)
        except Account.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None