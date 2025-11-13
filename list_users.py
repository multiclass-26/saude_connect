#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import Usuario

print("\n=== USUÁRIOS NO BANCO DE DADOS ===\n")

usuarios = Usuario.objects.all()

if usuarios.exists():
    for user in usuarios:
        print(f"✓ Username: {user.username} | Tipo: {user.tipo} | Nome: {user.first_name} {user.last_name}")
else:
    print("⚠️  Nenhum usuário encontrado. Execute: python manage.py create_users")

print("\n" + "="*50 + "\n")
