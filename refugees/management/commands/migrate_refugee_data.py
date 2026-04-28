"""
Script de migração de dados para criptografia AES-256.

Execução obrigatória APÓS a migração 0003 e ANTES da migração 0004:

    python manage.py migrate refugees 0003
    python manage.py migrate_refugee_data
    python manage.py migrate refugees 0004

O script lê os campos plaintext do banco via SQL direto, criptografa os valores
usando a mesma chave configurada em FIELD_ENCRYPTION_KEY e grava nas colunas
temporárias _enc. Funciona independentemente do estado atual do models.py.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from encrypted_model_fields.fields import encrypt_str

PLAINTEXT_FIELDS = [
    'name',
    'address',
    'age',
    'religion',
    'political_affiliation',
    'profession',
    'number_of_children',
    'family_income',
    'education_level',
]

ENC_FIELDS = [f'{field}_enc' for field in PLAINTEXT_FIELDS]


def _columns_exist(cursor, table, columns):
    cursor.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = %s",
        [table],
    )
    existing = {row[0] for row in cursor.fetchall()}
    return all(col in existing for col in columns)


def _sqlite_columns_exist(cursor, table, columns):
    cursor.execute(f"PRAGMA table_info({table})")
    existing = {row[1] for row in cursor.fetchall()}
    return all(col in existing for col in columns)


class Command(BaseCommand):
    help = (
        'Migra dados plaintext para campos criptografados. '
        'Execute após a migração 0003 e antes da 0004.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Exibe o que seria feito sem gravar no banco.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        table = 'refugees_refugees'

        with connection.cursor() as cursor:
            # Detecta backend e verifica existência das colunas necessárias
            vendor = connection.vendor
            if vendor == 'sqlite':
                has_plain = _sqlite_columns_exist(cursor, table, PLAINTEXT_FIELDS)
                has_enc = _sqlite_columns_exist(cursor, table, ENC_FIELDS)
            else:
                has_plain = _columns_exist(cursor, table, PLAINTEXT_FIELDS)
                has_enc = _columns_exist(cursor, table, ENC_FIELDS)

        if not has_enc:
            raise CommandError(
                'Colunas _enc não encontradas. '
                'Aplique a migração 0003 primeiro:\n'
                '    python manage.py migrate refugees 0003'
            )

        if not has_plain:
            raise CommandError(
                'Colunas plaintext não encontradas — a migração 0004 já foi aplicada '
                'ou os dados já foram migrados. Nada a fazer.'
            )

        with connection.cursor() as cursor:
            select_cols = ', '.join(['id'] + PLAINTEXT_FIELDS)
            cursor.execute(f'SELECT {select_cols} FROM {table}')
            rows = cursor.fetchall()

        total = len(rows)
        if total == 0:
            self.stdout.write(self.style.WARNING('Nenhum registro encontrado. Nada a migrar.'))
            return

        self.stdout.write(f'Migrando {total} registro(s)...')

        errors = 0
        for i, row in enumerate(rows, start=1):
            refugee_id = row[0]
            values = row[1:]

            try:
                encrypted = []
                for val in values:
                    if val is None:
                        encrypted.append(None)
                    else:
                        encrypted.append(encrypt_str(str(val)).decode('utf-8'))

                if not dry_run:
                    set_clause = ', '.join(f'{col} = %s' for col in ENC_FIELDS)
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f'UPDATE {table} SET {set_clause} WHERE id = %s',
                            [*encrypted, refugee_id],
                        )

                if dry_run:
                    self.stdout.write(f'  [dry-run] id={refugee_id} seria criptografado.')
                elif i % 100 == 0 or i == total:
                    self.stdout.write(f'  {i}/{total} registros processados.')

            except Exception as exc:
                self.stderr.write(
                    self.style.ERROR(f'  Erro no registro id={refugee_id}: {exc}')
                )
                errors += 1

        if errors:
            raise CommandError(
                f'Migração concluída com {errors} erro(s). '
                'Corrija os erros antes de aplicar a migração 0004.'
            )

        if dry_run:
            self.stdout.write(self.style.SUCCESS('Dry-run concluído. Nenhuma alteração foi feita.'))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nMigração concluída com sucesso ({total} registro(s)).\n'
                    'Agora aplique a migração 0004:\n'
                    '    python manage.py migrate refugees 0004'
                )
            )
