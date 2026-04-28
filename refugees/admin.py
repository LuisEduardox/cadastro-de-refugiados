from django.contrib import admin
from .models import Refugees


@admin.register(Refugees)
class RefugeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'profession', 'get_education_level_display', 'deleted_at')
    list_display_links = ('id', 'user', 'name')
    readonly_fields = ('deleted_at',)
    # Campos criptografados não suportam filtragem/ordenação por valor no banco.
    # search_fields e list_filter são intencionalmente omitidos para esses campos.
    ordering = ('-id',)
