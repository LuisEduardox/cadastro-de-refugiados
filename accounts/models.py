from django.contrib.auth.models import ABstractUser
from django.db import models
class User(ABstractUser):
    username = None
    email = models.models.EmailField(_("Email"), max_length=254, unique = True)
    