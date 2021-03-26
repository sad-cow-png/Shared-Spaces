
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create user with either as a client or proprietor
class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_proprietor = models.BooleanField(default=False)
