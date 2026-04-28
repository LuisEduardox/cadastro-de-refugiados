"""
Passo 2 de 2 da migração para criptografia.

IMPORTANTE: Execute 'python manage.py migrate_refugee_data' antes desta migração.

Remove as colunas plaintext antigas, renomeia as _enc para os nomes originais
e aplica constraints de NOT NULL e choices nos campos.
"""

import encrypted_model_fields.fields
from django.db import migrations
import refugees.fields


class Migration(migrations.Migration):

    dependencies = [
        ('refugees', '0003_add_encrypted_fields'),
    ]

    operations = [
        # Remove colunas plaintext
        migrations.RemoveField(model_name='refugees', name='name'),
        migrations.RemoveField(model_name='refugees', name='address'),
        migrations.RemoveField(model_name='refugees', name='age'),
        migrations.RemoveField(model_name='refugees', name='religion'),
        migrations.RemoveField(model_name='refugees', name='political_affiliation'),
        migrations.RemoveField(model_name='refugees', name='profession'),
        migrations.RemoveField(model_name='refugees', name='number_of_children'),
        migrations.RemoveField(model_name='refugees', name='family_income'),
        migrations.RemoveField(model_name='refugees', name='education_level'),

        # Renomeia _enc para nomes originais
        migrations.RenameField(model_name='refugees', old_name='name_enc', new_name='name'),
        migrations.RenameField(model_name='refugees', old_name='address_enc', new_name='address'),
        migrations.RenameField(model_name='refugees', old_name='age_enc', new_name='age'),
        migrations.RenameField(model_name='refugees', old_name='religion_enc', new_name='religion'),
        migrations.RenameField(model_name='refugees', old_name='political_affiliation_enc', new_name='political_affiliation'),
        migrations.RenameField(model_name='refugees', old_name='profession_enc', new_name='profession'),
        migrations.RenameField(model_name='refugees', old_name='number_of_children_enc', new_name='number_of_children'),
        migrations.RenameField(model_name='refugees', old_name='family_income_enc', new_name='family_income'),
        migrations.RenameField(model_name='refugees', old_name='education_level_enc', new_name='education_level'),

        # Aplica definições finais (NOT NULL + choices)
        migrations.AlterField(
            model_name='refugees',
            name='name',
            field=encrypted_model_fields.fields.EncryptedCharField(),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='address',
            field=encrypted_model_fields.fields.EncryptedCharField(),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='age',
            field=encrypted_model_fields.fields.EncryptedIntegerField(),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='religion',
            field=encrypted_model_fields.fields.EncryptedCharField(
                choices=[('MU', 'Mulçumano'), ('JU', 'Judeu'), ('CA', 'Católico')],
            ),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='political_affiliation',
            field=encrypted_model_fields.fields.EncryptedCharField(
                choices=[('ES', 'Esquerda'), ('DI', 'Direita'), ('CE', 'CENTRO')],
            ),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='profession',
            field=encrypted_model_fields.fields.EncryptedCharField(),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='number_of_children',
            field=encrypted_model_fields.fields.EncryptedIntegerField(),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='family_income',
            field=refugees.fields.EncryptedDecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AlterField(
            model_name='refugees',
            name='education_level',
            field=encrypted_model_fields.fields.EncryptedCharField(
                choices=[
                    ('sem', 'Sem escolaridade'),
                    ('efi', 'Ensino fundamental incompleto'),
                    ('efc', 'Ensino fundamental completo'),
                    ('emi', 'Ensino médio incompleto'),
                    ('emc', 'Ensino médio completo'),
                    ('esi', 'Ensino superior incompleto'),
                    ('esc', 'Ensino superior completo'),
                ],
            ),
        ),
    ]
