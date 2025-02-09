from django.db import models
from django.utils.translation import gettext_lazy as _
from Users.models import Account

class UserCrop(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_("User"))
    crop = models.CharField(max_length=100, verbose_name=_("Crop"))
    planting_date = models.DateField(verbose_name=_("Planting Date"))
    last_notified_stage = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Last Notified Stage"))  # To track the last notification

    def __str__(self):
        return f"{self.user.full_name()}'s {self.crop}"
    
    class Meta:
        verbose_name = _("User Crop")
        verbose_name_plural = _("User Crops")