from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager:
    def create_user(self,email, password = None):
        if not email:
            raise ValueError("email obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
              
class Admin(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
class User(AbstractUser):
    username = None