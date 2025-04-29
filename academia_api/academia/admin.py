from django.contrib import admin
from .models import Usuario, Plano, Pagamento, Presenca


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Exibir essas colunas na listagem
    list_display = ('aluno', 'email', 'tipo')


@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'preco')


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'valor', 'data_pagamento')


@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'data')
