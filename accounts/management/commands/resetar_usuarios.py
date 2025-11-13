"""
Comando Django para criar/resetar usuários
Uso: python manage.py resetar_usuarios
"""
from django.core.management.base import BaseCommand
from accounts.models import Usuario, AgenteSaude, Medico


class Command(BaseCommand):
    help = 'Cria/reseta usuários para acesso ao sistema'

    def handle(self, *args, **options):
        self.stdout.write('\n🔧 Resetando usuários...\n')
        
        usuarios = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@saude.gov.br',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'cpf': '000.000.000-00',
                'tipo': 'MEDICO',
                'is_superuser': True,
                'is_staff': True
            },
            {
                'username': 'medico',
                'password': 'medico123',
                'email': 'medico@saude.gov.br',
                'first_name': 'Dr. Carlos',
                'last_name': 'Silva',
                'cpf': '111.111.111-11',
                'tipo': 'MEDICO'
            },
            {
                'username': 'agente',
                'password': 'agente123',
                'email': 'paulo@saude.gov.br',
                'first_name': 'Paulo',
                'last_name': 'Silva',
                'cpf': '222.222.222-22',
                'tipo': 'AGENTE'
            },
            {
                'username': 'andre_agente',
                'password': 'agente123',
                'email': 'andre@saude.gov.br',
                'first_name': 'André',
                'last_name': 'Santos',
                'cpf': '333.333.333-33',
                'tipo': 'AGENTE'
            },
            {
                'username': 'fernanda_agente',
                'password': 'agente123',
                'email': 'fernanda@saude.gov.br',
                'first_name': 'Fernanda',
                'last_name': 'Costa',
                'cpf': '444.444.444-44',
                'tipo': 'AGENTE'
            },
            {
                'username': 'paciente',
                'password': 'paciente123',
                'email': 'paciente@email.com',
                'first_name': 'João',
                'last_name': 'Oliveira',
                'cpf': '555.555.555-55',
                'tipo': 'PACIENTE'
            }
        ]
        
        for dados in usuarios:
            try:
                # Buscar ou criar usuário
                usuario, created = Usuario.objects.get_or_create(
                    username=dados['username'],
                    defaults={
                        'email': dados['email'],
                        'first_name': dados['first_name'],
                        'last_name': dados['last_name'],
                        'cpf': dados['cpf'],
                        'tipo': dados['tipo'],
                        'is_superuser': dados.get('is_superuser', False),
                        'is_staff': dados.get('is_staff', False)
                    }
                )
                
                # Resetar senha
                usuario.set_password(dados['password'])
                if not created:
                    usuario.email = dados['email']
                    usuario.first_name = dados['first_name']
                    usuario.last_name = dados['last_name']
                    usuario.tipo = dados['tipo']
                    usuario.is_superuser = dados.get('is_superuser', False)
                    usuario.is_staff = dados.get('is_staff', False)
                usuario.save()
                
                # Criar perfil se necessário
                if dados['tipo'] == 'MEDICO':
                    if not hasattr(usuario, 'medico'):
                        crm = f'CRM-{usuario.id:05d}'
                        Medico.objects.create(usuario=usuario, crm=crm)
                        self.stdout.write(f'  ✓ Perfil médico criado para {dados["username"]}')
                
                elif dados['tipo'] == 'AGENTE':
                    if not hasattr(usuario, 'agente'):
                        id_agente = f'ACS-{usuario.id:03d}'
                        AgenteSaude.objects.create(usuario=usuario, id_agente=id_agente)
                        self.stdout.write(f'  ✓ Perfil agente criado para {dados["username"]}')
                
                status = 'criado' if created else 'atualizado'
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Usuário {dados["username"]} {status} - Senha: {dados["password"]}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro com {dados["username"]}: {str(e)}')
                )
        
        self.stdout.write('\n' + self.style.SUCCESS('📋 CREDENCIAIS PARA LOGIN:\n'))
        self.stdout.write('MÉDICOS:')
        self.stdout.write('  • admin / admin123 (Superusuário)')
        self.stdout.write('  • medico / medico123')
        self.stdout.write('\nAGENTES DE SAÚDE:')
        self.stdout.write('  • agente / agente123 (Paulo)')
        self.stdout.write('  • andre_agente / agente123 (André)')
        self.stdout.write('  • fernanda_agente / agente123 (Fernanda)')
        self.stdout.write('\nPACIENTE:')
        self.stdout.write('  • paciente / paciente123')
        self.stdout.write(self.style.SUCCESS('\n✅ Usuários prontos para login!\n'))
