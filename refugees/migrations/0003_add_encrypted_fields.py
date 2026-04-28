"""
Passo 1 de 2 da migração para criptografia.

Adiciona colunas temporárias com sufixo _enc para cada campo sensível.
Após aplicar esta migração, execute o script de migração de dados:

    python manage.py migrate_refugee_data

Só então aplique a migração 0004_finalize_encryption.
"""

import encrypted_model_fields.fields
from django.db import migrations
import refugees.fields


class Migration(migrations.Migration):

    dependencies = [
        ('refugees', '0002_refugees_deleted_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='refugees',
            name='name_enc',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='address_enc',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='age_enc',
            field=encrypted_model_fields.fields.EncryptedIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='religion_enc',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='political_affiliation_enc',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='profession_enc',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='number_of_children_enc',
            field=encrypted_model_fields.fields.EncryptedIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='family_income_enc',
            field=refugees.fields.EncryptedDecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='refugees',
            name='education_level_enc',
            field=encrypted_model_fields.fields.EncryptedCharField(blank=True, null=True),
        ),
    ]
