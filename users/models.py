from django.db import models
import uuid
from datetime import timedelta
from django.utils.timezone import now

# Create your models here.

from django.utils import timezone
# from common.utils.create_unique_code import get_otp_code
class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    failed_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
    def is_locked(self):
        return self.lock_until and now() < self.lock_until

