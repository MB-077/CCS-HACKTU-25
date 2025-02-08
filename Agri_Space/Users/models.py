from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone_number, email=None, password=None):
        if not phone_number:
            raise ValueError('Users must have an phone number')
        if not first_name:
            raise ValueError('Users must have a first name')
        
        email = self.normalize_email(email) if email else None
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, phone_number, email=None, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            password=password,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    phone_number = models.CharField(max_length=50, unique=True, verbose_name=_('Phone Number'))
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True, verbose_name=_('Email'))
    
    # required
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Joined'))
    last_login = models.DateTimeField(auto_now=True, verbose_name=_('Last Login'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Admin'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff'))
    is_active = models.BooleanField(default=False, verbose_name=_('Active'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Superuser'))
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    objects = MyAccountManager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.full_name()
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
     
        
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    address_line_1 = models.CharField(max_length=100, blank=True, verbose_name=_('Address Line 1'))
    address_line_2 = models.CharField(max_length=100, blank=True, verbose_name=_('Address Line 2'))
    profile_picture = models.ImageField(upload_to='userprofile', null=True, blank=True, default='userprofile/userprofile.jpg', verbose_name=_('Profile Picture'))
    country = models.CharField(max_length=50, blank=True, default='India', verbose_name=_('Country'))
    state = models.CharField(max_length=50, blank=True, verbose_name=_('State'))
    city = models.CharField(max_length=50, blank=True, verbose_name=_('City'))
    district = models.CharField(max_length=50, blank=True, verbose_name=_('District'))
    postal_code = models.CharField(max_length=50, blank=True, verbose_name=_('Postal Code'))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_('Longitude'))
    
    def __str__(self):
        return f"{self.user.first_name}"
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        

class UserImportantDetails(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='important_details', verbose_name=_('User'))
    state = models.CharField(max_length=50, blank=True, verbose_name=_('State'))
    crop_grown = models.CharField(max_length=50, blank=True, verbose_name=_('Crop Grown'))
    land_area = models.FloatField(blank=True, null=True, default=0, verbose_name=_('Land Area'))
    planting_date = models.DateField(blank=True, null=True, verbose_name=_('Planting Date'))
    receive_email = models.BooleanField(default=True, verbose_name=_('Receive Email'))
    receive_push_notification = models.BooleanField(default=False, verbose_name=_('Receive Push Notification'))
    receive_sms = models.BooleanField(default=False, verbose_name=_('Receive SMS'))
    
    def __str__(self):
        return f"{self.user.full_name()}'s Important Details"
    
    class Meta:
        verbose_name = _('User Important Detail')
        verbose_name_plural = _('User Important Details')
        

class TokenUsageLog(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name=_('Token'))
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('User'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'))
    user_agent = models.CharField(max_length=255, verbose_name=_('User Agent'))
    path = models.CharField(max_length=255, verbose_name=_('Path'))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_('Timestamp'))
    
    def __str__(self):
        return f"{self.user.full_name()} - {self.timestamp}"
    
    class Meta:
        verbose_name = _('Token Usage Log')
        verbose_name_plural = _('Token Usage Logs')
        

class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    online_status = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    
    def getonlinestatus(self):
        if self.online_status:
            return 'Online'
        return 'Offline'
    
    def __str__(self):
        return f"{self.user.full_name()} is {self.getonlinestatus()}"
    
    class Meta:
        verbose_name = _('User Status')
        verbose_name_plural = _('User Statuses')