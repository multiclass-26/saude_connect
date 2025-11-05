from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Medico, AgenteSaude

# Register your models here.


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo', 'cpf']
    list_filter = ['tipo', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo', 'cpf', 'endereco')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo', 'cpf', 'endereco')}),
    )

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'crm']
    search_fields = ['crm', 'usuario__first_name', 'usuario__last_name']

@admin.register(AgenteSaude)
class AgenteSaudeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'id_agente']
    search_fields = ['id_agente', 'usuario__first_name', 'usuario__last_name']
