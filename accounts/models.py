from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        (0, 'User'),
        (1, 'Admin'),
    )

    role = models.IntegerField(choices=ROLE_CHOICES, default=0)

    def __str__(self):
        return self.username