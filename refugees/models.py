from django.db import models
from .choices import Religions, PoliticalAffiliations, EducationLevels
from accounts.models import User
# Create your models here.

class Refugees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    address = models.CharField(max_length=250)
    age = models.IntegerField()
    religion = models.CharField(max_length=2, choices=Religions.choices)
    political_affiliation = models.CharField(max_length=2, choices=PoliticalAffiliations.choices)
    profession = models.CharField(max_length=100)
    number_of_children = models.IntegerField()
    family_income = models.DecimalField(max_digits=7, decimal_places=2)
    education_level = models.CharField(max_length=3, choices=EducationLevels.choices)
