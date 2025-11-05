from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'idade', 'cpf', 'cidade', 'bairro', 'criado_em']
    list_filter = ['cidade', 'comorbidade', 'fuma', 'bebe', 'atividade_fisica']
    search_fields = ['nome', 'cpf']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('usuario', 'agente', 'foto', 'nome', 'idade', 'peso', 'cpf', 'pessoas_na_casa')
        }),
        ('Localização', {
            'fields': ('cidade', 'bairro', 'endereco')
        }),
        ('Histórico Médico', {
            'fields': ('comorbidade', 'comorbidade_tipo', 'teve_avc', 'teve_infarto')
        }),
        ('Hábitos', {
            'fields': ('bebe', 'tipo_bebida', 'fuma', 'cigarros_por_dia', 'anos_fumando')
        }),
        ('Medicação e Alergias', {
            'fields': ('medicamentos', 'alergia', 'alergia_tipo')
        }),
        ('Atividade Física', {
            'fields': ('atividade_fisica', 'atividade_tipo', 'atividade_frequencia')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
