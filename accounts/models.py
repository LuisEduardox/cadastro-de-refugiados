from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField("nome de usuário", max_length=254, unique=False)
    email = models.EmailField("Email", max_length=254, unique = True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
