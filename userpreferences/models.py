from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class UserPreference(models.Model):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, default="USD", blank=True, null=True)

    def __str__(self):
        return str(self.user) +"'s preference"
