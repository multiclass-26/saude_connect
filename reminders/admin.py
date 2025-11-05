from django.contrib import admin
from .models import Alarme

@admin.register(Alarme)
class AlarmeAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'medicamento', 'data_hora', 'ativo', 'notificado']
    list_filter = ['ativo', 'notificado', 'data_hora']
    search_fields = ['medicamento', 'paciente__username']
    date_hierarchy = 'data_hora'
