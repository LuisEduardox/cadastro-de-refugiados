from django.db import models

class Religions(models.TextChoices):
    MULCUMANO = 'MU', 'Mulçumano'
    JUDEU = 'JU', 'Judeu'
    CATOLICO = 'CA', 'Católico'

class PoliticalAffiliations(models.TextChoices):
    ESQUERDA = 'ES', 'Esquerda'
    DIREITA = 'DI', 'Direita'
    CENTRO = 'CE', 'CENTRO'

class EducationLevels(models.TextChoices):
    SEM_ESCOLARIDADE = "sem", "Sem escolaridade",
    ENSINO_FUNDAMENTAL_INCOMPLETO = "efi","Ensino fundamental incompleto"
    ENSINO_FUNDAMENTAL_COMPLETO = "efc", "Ensino fundamental completo"
    ENSINO_MEDIO_INCOMPLETO = "emi", "Ensino médio incompleto"
    ENSINO_MEDIO_COMPLETO = "emc", "Ensino médio completo"
    ENSINO_SUPERIOR_INCOMPLETO = "esi", "Ensino superior incompleto"
    ENSINO_SUPERIOR_COMPLETO = "esc", "Ensino superior completo"