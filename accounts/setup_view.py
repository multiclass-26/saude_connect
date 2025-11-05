from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Usuario, Medico, AgenteSaude
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
                html += "<p>✓ Agente criado</p>"
            else:
                html += "<p>Agente já existe</p>"

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
                html += "<p>✓ Paciente criado</p>"
            else:
                html += "<p>Paciente já existe</p>"

        html += "<h2 style='color: green;'>✅ SETUP CONCLUÍDO!</h2>"
        html += "<h3>Credenciais de Acesso:</h3>"
        html += "<ul>"
        html += "<li><strong>Admin:</strong> admin / 123</li>"
        html += "<li><strong>Médico:</strong> CRM12345 / 123</li>"
        html += "<li><strong>Agente:</strong> AG001 / 123</li>"
        html += "<li><strong>Paciente:</strong> 111.222.333-44 / 123</li>"
        html += "</ul>"
        html += "<p><a href='/login/'>Ir para Login</a></p>"
        
    except Exception as e:
        html += f"<p style='color: red;'>❌ Erro: {str(e)}</p>"
    
    html += "</body></html>"
    return HttpResponse(html)
