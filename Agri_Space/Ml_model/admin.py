from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin

class UserCropAdmin(ModelAdmin):
    list_display = ('user', 'crop', 'planting_date', 'last_notified_stage')
    list_filter = ('user', 'crop', 'planting_date', 'last_notified_stage')
    search_fields = ('user', 'crop', 'planting_date', 'last_notified_stage')
    ordering = ('planting_date',)
    
admin.site.register(UserCrop, UserCropAdmin)