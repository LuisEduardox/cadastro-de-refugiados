from django.db import models
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedCharField, EncryptedIntegerField
from .choices import Religions, PoliticalAffiliations, EducationLevels
from .fields import EncryptedDecimalField
from accounts.models import User


class ActiveRefugeesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Refugees(models.Model):
    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    name = EncryptedCharField(max_length=150, null=False, blank=False)
    address = EncryptedCharField(max_length=250)
    age = EncryptedIntegerField()
    religion = EncryptedCharField(max_length=2, choices=Religions.choices)
    political_affiliation = EncryptedCharField(max_length=2, choices=PoliticalAffiliations.choices)
    profession = EncryptedCharField(max_length=100)
    number_of_children = EncryptedIntegerField()
    family_income = EncryptedDecimalField(max_digits=7, decimal_places=2)
    education_level = EncryptedCharField(max_length=3, choices=EducationLevels.choices)
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
