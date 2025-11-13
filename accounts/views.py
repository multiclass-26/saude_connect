from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Usuario, Medico, AgenteSaude
from django.db import transaction

# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        identificador = request.POST.get('identificador')
        senha = request.POST.get('senha')
        
        # Tenta autenticar diretamente com o username
        user = authenticate(request, username=identificador, password=senha)
        
        if user is not None:
            login(request, user)
            # Manter sessão ativa por 30 dias
            request.session.set_expiry(2592000)  # 30 dias em segundos
            messages.success(request, 'Login bem-sucedido!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'login.html')

def registro_view(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        endereco = request.POST.get('endereco')
        senha = request.POST.get('senha')
        
        try:
            with transaction.atomic():
                username = cpf.replace('.', '').replace('-', '')
                
                user = Usuario.objects.create_user(
                    username=username,
                    email=email,
                    password=senha,
                    first_name=nome.split()[0] if nome else '',
                    last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else '',
                    tipo=tipo.upper(),
                    cpf=cpf,
                    endereco=endereco
                )
                
                if tipo == 'medico':
                    crm = request.POST.get('crm')
                    Medico.objects.create(usuario=user, crm=crm)
                elif tipo == 'agente':
                    id_agente = request.POST.get('id')
                    AgenteSaude.objects.create(usuario=user, id_agente=id_agente)
                
                messages.success(request, f'{tipo.capitalize()} registrado com sucesso!')
                return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao registrar: {str(e)}')
    
    return render(request, 'registro.html')

@login_required
def dashboard_view(request):
    user = request.user
    
    if user.tipo == 'MEDICO':
        return redirect('dashboard_medico')
    elif user.tipo == 'AGENTE':
        return redirect('dashboard_agente')
    elif user.tipo == 'PACIENTE':
        return redirect('dashboard_paciente')
    
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')

def comunidade_view(request):
    # Página pública - não requer login
    return render(request, 'comunidade.html')

def informacoes_view(request):
    # Página pública - não requer login
    return render(request, 'informacoes.html')

@login_required
def perfil_view(request):
    user = request.user
    
    # Dados fictícios baseados no tipo de usuário
    context = {
        'user': user,
    }
    
    if user.tipo == 'MEDICO':
        try:
            medico = Medico.objects.get(usuario=user)
            context.update({
                'crm': medico.crm,
                'especialidade': 'Clínica Geral',
                'tempo_atuacao': '15 anos',
                'formacao': 'Universidade Federal de São Paulo (UNIFESP)',
                'telefone': '(11) 98765-4321',
            })
        except Medico.DoesNotExist:
            pass
    
    elif user.tipo == 'AGENTE':
        try:
            agente = AgenteSaude.objects.get(usuario=user)
            context.update({
                'id_agente': agente.id_agente,
                'area_atuacao': 'Centro - Zona Norte',
                'tempo_servico': '8 anos',
                'familias_atendidas': 45,
                'telefone': '(11) 98765-1234',
            })
        except AgenteSaude.DoesNotExist:
            pass
    
    elif user.tipo == 'PACIENTE':
        context.update({
            'data_nascimento': '15/03/1985',
            'idade': '40 anos',
            'tipo_sanguineo': 'O+',
            'alergias': 'Nenhuma alergia conhecida',
            'telefone': '(11) 98765-5678',
            'contato_emergencia': '(11) 98765-8765',
        })
    
    return render(request, 'perfil.html', context)

@login_required
def mapa_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'mapa.html', context)
