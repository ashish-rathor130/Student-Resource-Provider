from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
   email = models.EmailField(unique=True)
   is_email_verified = models.BooleanField(default=False)
   email_otp = models.CharField(max_length=6, null=True, blank=True)
   otp_last_sent = models.DateTimeField(null=True, blank=True) 
   
   