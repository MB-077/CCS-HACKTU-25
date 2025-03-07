from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy
from unfold.admin import ModelAdmin as UnfoldModelAdmin

class AccountAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'is_active', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_superuser')
    list_display_links = ('email', 'first_name', 'last_name')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_admin', 'is_staff', 'is_superuser', 'is_active')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    filter_horizontal = ()
    list_filter = ()
    
admin.site.register(Account, AccountAdmin)


class UserProfileAdmin(ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius: 50px;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'country', 'state', 'city', 'district', 'postal_code',)
    list_display_links = ('thumbnail', 'user',)
    list_filter = ('city', 'state', 'country')
    
admin.site.register(UserProfile, UserProfileAdmin)


admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class UserImportantDetailsAdmin(ModelAdmin):
    list_display = ('user', 'state', 'crop_grown', 'planting_date', 'land_area', 'receive_email', 'receive_push_notification', 'receive_sms',)
    list_filter = ('state', 'planting_date',)
    search_fields = ('user', 'state', 'crop_grown',)
    
admin.site.register(UserImportantDetails, UserImportantDetailsAdmin)


class TokenProxyAdmin(UnfoldModelAdmin):
    list_display = ('key', 'user', 'created',)
    search_fields = ('key', 'user',)
    list_filter = ('created',)
    readonly_fields = ('key', 'user', 'created',)
    ordering = ('-created',)
    
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, TokenProxyAdmin)


class UserStatusAdmin(ModelAdmin):
    list_display = ('user', 'online_status', 'last_login',)
    list_filter = ('online_status', 'last_login',)
    search_fields = ('user',)
    
admin.site.register(UserStatus, UserStatusAdmin)


class StateDataAdmin(ModelAdmin):
    list_display = ('indian_state', 'soil_type', 'avg_monthly_rainfall',)
    
admin.site.register(StateData, StateDataAdmin)