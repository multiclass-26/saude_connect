from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Usuario, Medico, AgenteSaude
from patients.models import Paciente
from reminders.models import Alarme
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

@csrf_exempt
def setup_view(request):
    """View temporária para criar dados de teste - REMOVER DEPOIS!"""
    
    html = "<html><body><h1>Setup de Dados de Teste</h1>"
    
    try:
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
                html += "<p>✓ Admin criado</p>"
            else:
                html += "<p>Admin já existe</p>"

            # Médico
            medico_user = None
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
                html += "<p>✓ Médico criado</p>"
            else:
                html += "<p>Médico já existe</p>"
                medico_user = Usuario.objects.get(username='12345678900')

            # Agente
            agente_user = None
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
                html += "<p>✓ Agente criado</p>"
            else:
                html += "<p>Agente já existe</p>"
                agente_user = Usuario.objects.get(username='98765432100')

            # Paciente
            paciente_user = None
            if not Usuario.objects.filter(username='11122233344').exists():
                paciente_user = Usuario.objects.create_user(
                    username='11122233344',
                    email='paciente@email.com',
                    password='123',
                    first_name='Joao',
                    last_name='Oliveira',
                    tipo='PACIENTE',
                    cpf='111.222.333-44',
                    endereco='Rua Nova, 789'
                )
                html += "<p>✓ Paciente criado</p>"
            else:
                html += "<p>Paciente já existe</p>"
                paciente_user = Usuario.objects.get(username='11122233344')

            # Criar pacientes de teste
            html += "<h3>Criando Pacientes...</h3>"
            
            if not Paciente.objects.filter(cpf='111.222.333-44').exists():
                p1 = Paciente.objects.create(
                    nome='Maria Silva',
                    cpf='111.222.333-44',
                    idade=59,
                    peso=68.5,
                    cidade='São Paulo',
                    bairro='Centro',
                    endereco='Rua das Flores, 100',
                    pessoas_na_casa=3,
                    comorbidade=True,
                    comorbidade_tipo='Hipertensão',
                    teve_avc=False,
                    teve_infarto=False,
                    medicamentos='Losartana 50mg - 1x ao dia',
                    fuma=False,
                    bebe=False,
                    atividade_fisica=True,
                    atividade_tipo='Caminhada',
                    atividade_frequencia='3x por semana',
                    agente=agente_user.agentesaude if agente_user and hasattr(agente_user, 'agentesaude') else None
                )
                html += "<p>✓ Paciente Maria Silva criado</p>"

            if not Paciente.objects.filter(cpf='222.333.444-55').exists():
                p2 = Paciente.objects.create(
                    nome='João Santos',
                    cpf='222.333.444-55',
                    idade=67,
                    peso=82.3,
                    cidade='São Paulo',
                    bairro='Jardins',
                    endereco='Av. Principal, 200',
                    pessoas_na_casa=2,
                    comorbidade=True,
                    comorbidade_tipo='Diabetes tipo 2',
                    teve_avc=False,
                    teve_infarto=False,
                    medicamentos='Metformina 850mg - 2x ao dia',
                    fuma=False,
                    cigarros_por_dia=0,
                    anos_fumando=0,
                    bebe=True,
                    tipo_bebida='Cerveja ocasionalmente',
                    atividade_fisica=False,
                    agente=agente_user.agentesaude if agente_user and hasattr(agente_user, 'agentesaude') else None
                )
                html += "<p>✓ Paciente João Santos criado</p>"

            if not Paciente.objects.filter(cpf='333.444.555-66').exists():
                p3 = Paciente.objects.create(
                    nome='Ana Costa',
                    cpf='333.444.555-66',
                    idade=53,
                    peso=61.2,
                    cidade='São Paulo',
                    bairro='Vila Mariana',
                    endereco='Rua Nova, 300',
                    pessoas_na_casa=4,
                    comorbidade=True,
                    comorbidade_tipo='DPOC (Doença Pulmonar Obstrutiva Crônica)',
                    teve_avc=False,
                    teve_infarto=False,
                    medicamentos='Broncodilatador - uso contínuo',
                    fuma=True,
                    cigarros_por_dia=10,
                    anos_fumando=20,
                    bebe=False,
                    atividade_fisica=False,
                    agente=agente_user.agentesaude if agente_user and hasattr(agente_user, 'agentesaude') else None
                )
                html += "<p>✓ Paciente Ana Costa criado</p>"

            if not Paciente.objects.filter(cpf='444.555.666-77').exists():
                p4 = Paciente.objects.create(
                    nome='Carlos Mendes',
                    cpf='444.555.666-77',
                    idade=35,
                    peso=78.0,
                    cidade='São Paulo',
                    bairro='Pinheiros',
                    endereco='Alameda das Árvores, 400',
                    pessoas_na_casa=1,
                    comorbidade=False,
                    teve_avc=False,
                    teve_infarto=False,
                    medicamentos='Nenhum',
                    fuma=False,
                    bebe=True,
                    tipo_bebida='Vinho socialmente',
                    atividade_fisica=True,
                    atividade_tipo='Musculação',
                    atividade_frequencia='5x por semana',
                    agente=agente_user.agentesaude if agente_user and hasattr(agente_user, 'agentesaude') else None
                )
                html += "<p>✓ Paciente Carlos Mendes criado</p>"

            if not Paciente.objects.filter(cpf='555.666.777-88').exists():
                p5 = Paciente.objects.create(
                    nome='Rosa Lima',
                    cpf='555.666.777-88',
                    idade=45,
                    peso=72.8,
                    cidade='São Paulo',
                    bairro='Mooca',
                    endereco='Travessa do Sol, 500',
                    pessoas_na_casa=3,
                    comorbidade=True,
                    comorbidade_tipo='Hipertensão',
                    teve_avc=True,
                    teve_infarto=False,
                    medicamentos='Losartana 100mg, AAS 100mg - uso contínuo',
                    fuma=False,
                    bebe=False,
                    atividade_fisica=True,
                    atividade_tipo='Hidroginástica',
                    atividade_frequencia='2x por semana',
                    agente=agente_user.agentesaude if agente_user and hasattr(agente_user, 'agentesaude') else None
                )
                html += "<p>✓ Paciente Rosa Lima criado</p>"

            # Criar alarmes de teste para o paciente
            if paciente_user:
                html += "<h3>Criando Lembretes...</h3>"
                
                if not Alarme.objects.filter(medicamento='Losartana 50mg').exists():
                    Alarme.objects.create(
                        paciente=paciente_user,
                        medicamento='Losartana 50mg',
                        data_hora=timezone.now().replace(hour=8, minute=0, second=0, microsecond=0),
                        ativo=True
                    )
                    html += "<p>✓ Lembrete Losartana criado</p>"

                if not Alarme.objects.filter(medicamento='Metformina 850mg').exists():
                    Alarme.objects.create(
                        paciente=paciente_user,
                        medicamento='Metformina 850mg',
                        data_hora=timezone.now().replace(hour=12, minute=0, second=0, microsecond=0),
                        ativo=True
                    )
                    html += "<p>✓ Lembrete Metformina criado</p>"

                if not Alarme.objects.filter(medicamento='Sinvastatina 20mg').exists():
                    Alarme.objects.create(
                        paciente=paciente_user,
                        medicamento='Sinvastatina 20mg',
                        data_hora=timezone.now().replace(hour=20, minute=0, second=0, microsecond=0),
                        ativo=True
                    )
                    html += "<p>✓ Lembrete Sinvastatina criado</p>"

                if not Alarme.objects.filter(medicamento='Omeprazol 20mg').exists():
                    Alarme.objects.create(
                        paciente=paciente_user,
                        medicamento='Omeprazol 20mg',
                        data_hora=timezone.now().replace(hour=7, minute=30, second=0, microsecond=0),
                        ativo=True
                    )
                    html += "<p>✓ Lembrete Omeprazol criado</p>"

        html += "<h2 style='color: green;'>✅ SETUP COMPLETO CONCLUÍDO!</h2>"
        html += "<h3>Credenciais de Acesso:</h3>"
        html += "<ul>"
        html += "<li><strong>Admin:</strong> admin / 123</li>"
        html += "<li><strong>Médico:</strong> CRM12345 / 123</li>"
        html += "<li><strong>Agente:</strong> AG001 / 123</li>"
        html += "<li><strong>Paciente:</strong> 111.222.333-44 / 123</li>"
        html += "</ul>"
        html += "<h3>Dados criados:</h3>"
        html += "<ul>"
        html += "<li>5 pacientes de teste</li>"
        html += "<li>4 lembretes de medicação</li>"
        html += "</ul>"
        html += "<p><a href='/login/'>Ir para Login</a></p>"
        
    except Exception as e:
        html += f"<p style='color: red;'>❌ Erro: {str(e)}</p>"
        import traceback
        html += f"<pre>{traceback.format_exc()}</pre>"
    
    html += "</body></html>"
    return HttpResponse(html)
