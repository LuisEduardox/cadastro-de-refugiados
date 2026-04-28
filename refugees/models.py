from django.db import models
from django.utils import timezone
from .choices import Religions, PoliticalAffiliations, EducationLevels
from accounts.models import User


class ActiveRefugeesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Refugees(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    address = models.CharField(max_length=250)
    age = models.IntegerField()
    religion = models.CharField(max_length=2, choices=Religions.choices)
    political_affiliation = models.CharField(max_length=2, choices=PoliticalAffiliations.choices)
    profession = models.CharField(max_length=100)
    number_of_children = models.IntegerField()
    family_income = models.DecimalField(max_digits=7, decimal_places=2)
    education_level = models.CharField(max_length=3, choices=EducationLevels.choices)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ActiveRefugeesManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
