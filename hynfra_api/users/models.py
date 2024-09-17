from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add custom fields if needed
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('standard', 'Standard User'),
        ('guest', 'Guest'),
        
    ], default="standard")

    class Meta:
        verbose_name = 'User'

    def is_admin(self):
        return self.role == 'admin'

    def is_standard_user(self):
        return self.role == 'standard'

    def is_guest(self):
        return self.role == 'guest'