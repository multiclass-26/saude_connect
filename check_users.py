#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Usuario, Medico, AgenteSaude

print("=" * 50)
print("VERIFICAÇÃO DE USUÁRIOS NO RAILWAY")
print("=" * 50)

total_usuarios = Usuario.objects.count()
print(f"\nTotal de usuários: {total_usuarios}")

if total_usuarios > 0:
    print("\n--- Usuários cadastrados ---")
    for usuario in Usuario.objects.all():
        print(f"  • {usuario.username} - {usuario.get_tipo_display()} - CPF: {usuario.cpf}")
        if usuario.tipo == 'MEDICO':
            try:
                medico = usuario.medico
                print(f"    CRM: {medico.crm}")
            except:
                print(f"    ⚠️ Sem perfil de médico associado!")
        elif usuario.tipo == 'AGENTE':
            try:
                agente = usuario.agente
                print(f"    ID Agente: {agente.id_agente}")
            except:
                print(f"    ⚠️ Sem perfil de agente associado!")
    
    print("\n--- Médicos ---")
    print(f"Total: {Medico.objects.count()}")
    for medico in Medico.objects.all():
        print(f"  • {medico.usuario.username} - CRM: {medico.crm}")
    
    print("\n--- Agentes de Saúde ---")
    print(f"Total: {AgenteSaude.objects.count()}")
    for agente in AgenteSaude.objects.all():
        print(f"  • {agente.usuario.username} - ID: {agente.id_agente}")
else:
    print("\n⚠️ NENHUM USUÁRIO ENCONTRADO!")
    print("Execute o comando: python manage.py create_users")

print("\n" + "=" * 50)
