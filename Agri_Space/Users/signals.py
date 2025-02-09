from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, UserProfile, UserStatus, Token, UserImportantDetails
from Ml_model.models import UserCrop
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone

@receiver(post_save, sender=Account)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
@receiver(post_save, sender=Account)
def update_user_status(sender, instance, created, **kwargs):
    if created:
        instance.is_active = True
        instance.save()


@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(
        user=user,
        defaults={'online_status': True, 'last_login': timezone.now()}
    )


@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(
        user=user,
        defaults={'online_status': False}
    )

@receiver(post_save, sender=UserImportantDetails)
def update_user_crop(sender, instance, created, **kwargs):
    UserCrop.objects.update_or_create(
        user=instance.user,
        crop=instance.crop_grown,
        planting_date=instance.planting_date
    )