from django.core.management.base import BaseCommand
from accounts.models import Usuario, Medico, AgenteSaude
from django.db import transaction

class Command(BaseCommand):
    help = 'Cria usuários de teste'

    def handle(self, *args, **kwargs):
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
                self.stdout.write(self.style.SUCCESS('✓ Admin criado'))

            # Médico
            if not Usuario.objects.filter(username='medico').exists():
                medico_user = Usuario.objects.create_user(
                    username='medico',
                    email='medico@saude.com',
                    password='123',
                    first_name='Carlos',
                    last_name='Silva',
                    tipo='MEDICO',
                    cpf='123.456.789-00',
                    endereco='Rua das Flores, 123'
                )
                Medico.objects.create(usuario=medico_user, crm='CRM12345')
                self.stdout.write(self.style.SUCCESS('✓ Médico criado (username: medico)'))

            # Agente
            if not Usuario.objects.filter(username='agente').exists():
                agente_user = Usuario.objects.create_user(
                    username='agente',
                    email='agente@saude.com',
                    password='123',
                    first_name='Maria',
                    last_name='Santos',
                    tipo='AGENTE',
                    cpf='987.654.321-00',
                    endereco='Av. Principal, 456'
                )
                AgenteSaude.objects.create(usuario=agente_user, id_agente='AG001')
                self.stdout.write(self.style.SUCCESS('✓ Agente criado (username: agente)'))

            # Paciente
            if not Usuario.objects.filter(username='paciente').exists():
                Usuario.objects.create_user(
                    username='paciente',
                    email='paciente@email.com',
                    password='123',
                    first_name='Joao',
                    last_name='Oliveira',
                    tipo='PACIENTE',
                    cpf='111.222.333-44',
                    endereco='Rua Nova, 789'
                )
                self.stdout.write(self.style.SUCCESS('✓ Paciente criado (username: paciente)'))

        self.stdout.write(self.style.SUCCESS('\n=== USUÁRIOS CRIADOS ==='))
