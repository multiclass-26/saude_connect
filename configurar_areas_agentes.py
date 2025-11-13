#!/usr/bin/env python
"""Script para configurar áreas dos agentes existentes"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Usuario, AgenteSaude

print('\n🔧 Configurando áreas dos agentes...\n')

# Configurar agente existente (Maria/agente) como Paulo
try:
    usuario_maria = Usuario.objects.get(username='agente')
    agente_maria = usuario_maria.agente
    
    # Renomear para Paulo
    usuario_maria.first_name = 'Paulo'
    usuario_maria.last_name = 'Silva'
    usuario_maria.save()
    
    agente_maria.area_nome = 'Área do Agente Paulo'
    agente_maria.area_coordenadas = [
        [-10.9420, -37.0680],
        [-10.9420, -37.0730],
        [-10.9470, -37.0730],
        [-10.9470, -37.0680]
    ]
    agente_maria.save()
    
    print(f'✓ Agente Paulo configurado (Username: agente)')
except Exception as e:
    print(f'❌ Erro ao configurar Paulo: {e}')

# Configurar André
try:
    usuario_andre = Usuario.objects.get(username='andre_agente')
    agente_andre = usuario_andre.agente
    
    agente_andre.area_nome = 'Área do Agente André'
    agente_andre.area_coordenadas = [
        [-10.9470, -37.0680],
        [-10.9470, -37.0730],
        [-10.9520, -37.0730],
        [-10.9520, -37.0680]
    ]
    agente_andre.save()
    
    print(f'✓ Agente André configurado')
except Exception as e:
    print(f'❌ Erro ao configurar André: {e}')

# Configurar Fernanda
try:
    usuario_fernanda = Usuario.objects.get(username='fernanda_agente')
    agente_fernanda = usuario_fernanda.agente
    
    agente_fernanda.area_nome = 'Área da Agente Fernanda'
    agente_fernanda.area_coordenadas = [
        [-10.9420, -37.0730],
        [-10.9420, -37.0780],
        [-10.9470, -37.0780],
        [-10.9470, -37.0730]
    ]
    agente_fernanda.save()
    
    print(f'✓ Agente Fernanda configurada')
except Exception as e:
    print(f'❌ Erro ao configurar Fernanda: {e}')

print('\n✅ Configuração concluída!')
print('\nAgentes disponíveis:')
print('  • Paulo (username: agente, senha: senha123)')
print('  • André (username: andre_agente, senha: saude123)')
print('  • Fernanda (username: fernanda_agente, senha: saude123)')
