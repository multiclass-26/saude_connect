from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Paciente
from accounts.models import AgenteSaude
from django.http import JsonResponse

@login_required
def dashboard_agente(request):
    if request.user.tipo != 'AGENTE':
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')
    
    agente = request.user.agente
    pacientes = Paciente.objects.filter(agente=agente)
    
    return render(request, 'patients/dashboard_agente.html', {'pacientes': pacientes})

@login_required
def dashboard_medico(request):
    if request.user.tipo != 'MEDICO':
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')
    
    search = request.GET.get('search', '')
    pacientes = Paciente.objects.all()
    
    if search:
        pacientes = pacientes.filter(
            Q(nome__icontains=search) | Q(cpf__icontains=search)
        )
    
    return render(request, 'patients/dashboard_medico.html', {
        'pacientes': pacientes,
        'search': search
    })

@login_required
def cadastrar_paciente(request):
    if request.user.tipo != 'AGENTE':
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            agente = request.user.agente
            
            paciente = Paciente(
                agente=agente,
                nome=request.POST.get('nome'),
                idade=request.POST.get('idade'),
                peso=request.POST.get('peso') or None,
                cpf=request.POST.get('cpf'),
                pessoas_na_casa=request.POST.get('pessoas') or None,
                cidade=request.POST.get('cidade'),
                bairro=request.POST.get('bairro'),
                endereco=request.POST.get('endereco'),
                comorbidade=request.POST.get('comorbidade') == 'on',
                comorbidade_tipo=request.POST.get('comorbidadeTipo', ''),
                teve_avc=request.POST.get('avc') == 'on',
                teve_infarto=request.POST.get('infarto') == 'on',
                bebe=request.POST.get('bebe') == 'on',
                tipo_bebida=request.POST.get('bebeTipo', ''),
                fuma=request.POST.get('fuma') == 'on',
                cigarros_por_dia=int(request.POST.get('cigarrosPorDia', 0) or 0),
                anos_fumando=int(request.POST.get('anosFumando', 0) or 0),
                medicamentos=request.POST.get('medicamento', ''),
                alergia=request.POST.get('alergia') == 'on',
                alergia_tipo=request.POST.get('alergiaTipo', ''),
                atividade_fisica=request.POST.get('atividade') == 'on',
                atividade_tipo=request.POST.get('atividadeTipo', ''),
                atividade_frequencia=request.POST.get('atividadeFrequencia', ''),
            )
            
            if request.FILES.get('foto'):
                paciente.foto = request.FILES['foto']
            
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('dashboard_agente')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar paciente: {str(e)}')
    
    return render(request, 'patients/cadastrar_paciente.html')

@login_required
def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    if request.user.tipo == 'AGENTE' and paciente.agente != request.user.agente:
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            paciente.nome = request.POST.get('nome')
            paciente.idade = request.POST.get('idade')
            paciente.peso = request.POST.get('peso') or None
            paciente.cpf = request.POST.get('cpf')
            paciente.endereco = request.POST.get('endereco')
            paciente.comorbidade = request.POST.get('comorbidade') == 'on'
            paciente.comorbidade_tipo = request.POST.get('comorbidadeTipo', '')
            paciente.teve_avc = request.POST.get('avc') == 'on'
            paciente.teve_infarto = request.POST.get('infarto') == 'on'
            paciente.bebe = request.POST.get('bebe') == 'on'
            paciente.tipo_bebida = request.POST.get('bebeTipo', '')
            paciente.fuma = request.POST.get('fuma') == 'on'
            paciente.cigarros_por_dia = int(request.POST.get('cigarrosPorDia', 0) or 0)
            paciente.anos_fumando = int(request.POST.get('anosFumando', 0) or 0)
            paciente.medicamentos = request.POST.get('medicamento', '')
            paciente.alergia = request.POST.get('alergia') == 'on'
            paciente.alergia_tipo = request.POST.get('alergiaTipo', '')
            paciente.atividade_fisica = request.POST.get('atividade') == 'on'
            paciente.atividade_tipo = request.POST.get('atividadeTipo', '')
            paciente.atividade_frequencia = request.POST.get('atividadeFrequencia', '')
            
            if request.FILES.get('foto'):
                paciente.foto = request.FILES['foto']
            
            paciente.save()
            messages.success(request, 'Paciente atualizado com sucesso!')
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def excluir_paciente(request, pk):
    if request.user.tipo != 'AGENTE':
        return JsonResponse({'success': False, 'error': 'Acesso negado'})
    
    paciente = get_object_or_404(Paciente, pk=pk, agente=request.user.agente)
    paciente.delete()
    messages.success(request, 'Paciente excluído com sucesso!')
    return JsonResponse({'success': True})
