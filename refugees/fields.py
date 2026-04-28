from encrypted_model_fields.fields import EncryptedMixin
from django.db import models


class EncryptedDecimalField(EncryptedMixin, models.DecimalField):
    """DecimalField com criptografia AES-256 via Fernet (django-encrypted-model-fields)."""
    pass
