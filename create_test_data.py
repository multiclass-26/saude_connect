#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Usuario, Medico, AgenteSaude
from patients.models import Paciente
from reminders.models import Alarme
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

print("=== CRIANDO DADOS DE TESTE ===\n")

# Criar usuários principais
with transaction.atomic():
    # Admin
    if not Usuario.objects.filter(username='admin').exists():
        Usuario.objects.create_superuser(
            username='admin',
            email='admin@saude.com',
            password='123',
            first_name='Admin',
            last_name='Sistema',
            tipo='MEDICO',
            cpf='000.000.000-00'
        )
        print("✓ Admin criado")

    # Médico
    if not Usuario.objects.filter(username='12345678900').exists():
        medico_user = Usuario.objects.create_user(
            username='12345678900',
            email='medico@saude.com',
            password='123',
            first_name='Carlos',
            last_name='Silva',
            tipo='MEDICO',
            cpf='123.456.789-00',
            endereco='Rua das Flores, 123'
        )
        Medico.objects.create(usuario=medico_user, crm='CRM12345')
        print("✓ Médico criado")

    # Agente
    if not Usuario.objects.filter(username='98765432100').exists():
        agente_user = Usuario.objects.create_user(
            username='98765432100',
            email='agente@saude.com',
            password='123',
            first_name='Maria',
            last_name='Santos',
            tipo='AGENTE',
            cpf='987.654.321-00',
            endereco='Av. Principal, 456'
        )
        AgenteSaude.objects.create(usuario=agente_user, id_agente='AG001')
        print("✓ Agente criado")

    # Paciente
    if not Usuario.objects.filter(username='11122233344').exists():
        Usuario.objects.create_user(
            username='11122233344',
            email='paciente@email.com',
            password='123',
            first_name='Joao',
            last_name='Oliveira',
            tipo='PACIENTE',
            cpf='111.222.333-44',
            endereco='Rua Nova, 789'
        )
        print("✓ Paciente criado")

print("\n=== DADOS CRIADOS COM SUCESSO ===")
