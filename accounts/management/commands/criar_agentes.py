from django.core.management.base import BaseCommand
from accounts.models import Usuario, AgenteSaude

class Command(BaseCommand):
    help = 'Cria agentes de saúde com áreas definidas'

    def handle(self, *args, **options):
        self.stdout.write('Criando agentes de saúde...')
        
        agentes_dados = [
            {
                'username': 'paulo_agente',
                'email': 'paulo@saude.gov.br',
                'first_name': 'Paulo',
                'last_name': 'Silva',
                'cpf': '111.222.333-44',
                'tipo': 'AGENTE',
                'id_agente': 'ACS001',
                'area_nome': 'Área do Agente Paulo',
                'area_coordenadas': [
                    [-10.9420, -37.0680],
                    [-10.9420, -37.0730],
                    [-10.9470, -37.0730],
                    [-10.9470, -37.0680]
                ]
            },
            {
                'username': 'andre_agente',
                'email': 'andre@saude.gov.br',
                'first_name': 'André',
                'last_name': 'Santos',
                'cpf': '222.333.444-55',
                'tipo': 'AGENTE',
                'id_agente': 'ACS002',
                'area_nome': 'Área do Agente André',
                'area_coordenadas': [
                    [-10.9470, -37.0680],
                    [-10.9470, -37.0730],
                    [-10.9520, -37.0730],
                    [-10.9520, -37.0680]
                ]
            },
            {
                'username': 'fernanda_agente',
                'email': 'fernanda@saude.gov.br',
                'first_name': 'Fernanda',
                'last_name': 'Costa',
                'cpf': '333.444.555-66',
                'tipo': 'AGENTE',
                'id_agente': 'ACS003',
                'area_nome': 'Área da Agente Fernanda',
                'area_coordenadas': [
                    [-10.9420, -37.0730],
                    [-10.9420, -37.0780],
                    [-10.9470, -37.0780],
                    [-10.9470, -37.0730]
                ]
            },
        ]
        
        for dados in agentes_dados:
            try:
                # Verificar se já existe
                if Usuario.objects.filter(username=dados['username']).exists():
                    self.stdout.write(self.style.WARNING(f'Usuário {dados["username"]} já existe. Pulando...'))
                    continue
                
                # Criar usuário
                usuario = Usuario.objects.create_user(
                    username=dados['username'],
                    email=dados['email'],
                    first_name=dados['first_name'],
                    last_name=dados['last_name'],
                    cpf=dados['cpf'],
                    tipo=dados['tipo'],
                    password='saude123'  # Senha padrão para demonstração
                )
                
                # Criar perfil de agente
                agente = AgenteSaude.objects.create(
                    usuario=usuario,
                    id_agente=dados['id_agente'],
                    area_nome=dados['area_nome'],
                    area_coordenadas=dados['area_coordenadas']
                )
                
                self.stdout.write(self.style.SUCCESS(f'✓ Agente criado: {dados["first_name"]} {dados["last_name"]} (Usuário: {dados["username"]}, Senha: saude123)'))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao criar {dados["username"]}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nAgentes criados com sucesso!'))
        self.stdout.write('Você pode fazer login com:')
        self.stdout.write('  paulo_agente / saude123')
        self.stdout.write('  andre_agente / saude123')
        self.stdout.write('  fernanda_agente / saude123')
