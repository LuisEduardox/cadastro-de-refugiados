from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from .choices import Role


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["role"] = Role.Admin
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField("nome de usuário", max_length=254, unique=False)
    email = models.EmailField("Email", max_length=254, unique=True)
    role = models.PositiveSmallIntegerField(
        choices=Role.choices,
        default=Role.Default_user
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.role == Role.Admin:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)
