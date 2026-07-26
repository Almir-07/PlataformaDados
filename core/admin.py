from django.contrib import admin
from .models import Arquivo, Cliente, Importacao


@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "idade")
    search_fields = ("nome", "email")
    list_filter = ("idade",)
    ordering = ("nome",)

@admin.register(Importacao)
class ImportacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "arquivo", "data", "importados", "ignorados")
    ordering = ("-data",)