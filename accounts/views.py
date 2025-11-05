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
        tipo = request.POST.get('tipo')
        identificador = request.POST.get('identificador')
        senha = request.POST.get('senha')
        
        try:
            if tipo == 'medico':
                medico = Medico.objects.get(crm=identificador)
                user = medico.usuario
            elif tipo == 'agente':
                agente = AgenteSaude.objects.get(id_agente=identificador)
                user = agente.usuario
            elif tipo == 'paciente':
                user = Usuario.objects.get(cpf=identificador, tipo='PACIENTE')
            else:
                messages.error(request, 'Tipo de usuário inválido.')
                return render(request, 'login.html')
            
            user = authenticate(request, username=user.username, password=senha)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login bem-sucedido!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciais inválidas.')
        except (Medico.DoesNotExist, AgenteSaude.DoesNotExist, Usuario.DoesNotExist):
            messages.error(request, 'Usuário não encontrado.')
    
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
