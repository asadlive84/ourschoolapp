from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


class UserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user_details")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number_first = models.CharField(max_length=50)
    phone_number_two = models.CharField(max_length=50, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    present_address = models.TextField()
    permanent_address = models.TextField()
