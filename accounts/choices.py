from django.db import models

class Role(models.IntegerChoices):
    Default_user = 1, "Usuário padrão"
    Admin = 2, "Administrador"