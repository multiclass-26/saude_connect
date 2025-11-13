from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Paciente, Residencia
from accounts.models import AgenteSaude
from django.http import JsonResponse


@login_required
def mapa_dados_agente(request):
    """API endpoint para dados do mapa - visão do agente"""
    if request.user.tipo != 'AGENTE':
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    agente = request.user.agente
    
    # Buscar pacientes do agente
    pacientes = Paciente.objects.filter(agente=agente).select_related('residencia')
    
    pacientes_data = []
    for p in pacientes:
        pacientes_data.append({
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'is_infantil': p.is_infantil,
            'cpf': p.cpf,
            'tipo_sanguineo': p.tipo_sanguineo,
            'endereco': p.endereco,
            'bairro': p.bairro,
            'latitude': float(p.latitude) if p.latitude else None,
            'longitude': float(p.longitude) if p.longitude else None,
            'residencia_id': p.residencia.id if p.residencia else None,
            'doenca_atual': p.doenca_atual,
            'nivel_gravidade': p.nivel_gravidade,
            'is_cronica': p.is_cronica,
            'is_contagiosa': p.is_contagiosa,
            'medicamentos': p.medicamentos,
            'medicamentos_prescritos': p.medicamentos_prescritos,
            'necessidades_basicas': p.necessidades_basicas,
            'recebe_auxilio_governo': p.recebe_auxilio_governo,
            'tipo_auxilio': p.tipo_auxilio,
            'tem_acamado': p.tem_acamado,
            'ultima_consulta': p.ultima_consulta.strftime('%d/%m/%Y') if p.ultima_consulta else None,
            'proxima_consulta': p.proxima_consulta.strftime('%d/%m/%Y') if p.proxima_consulta else None,
            'comorbidade': p.comorbidade,
            'comorbidade_tipo': p.comorbidade_tipo,
        })
    
    # Buscar residências da área
    residencias = Residencia.objects.filter(
        Q(agente=agente) | Q(agente__isnull=True, bairro__in=pacientes.values_list('bairro', flat=True).distinct())
    )
    
    residencias_data = []
    for r in residencias:
        residencias_data.append({
            'id': r.id,
            'endereco': f'{r.endereco_completo}, {r.numero}',
            'bairro': r.bairro,
            'status': r.status,
            'status_display': r.get_status_display(),
            'qtd_moradores': r.qtd_moradores,
            'latitude': float(r.latitude),
            'longitude': float(r.longitude),
            'cadastrada': r.status == 'CADASTRADA',
        })
    
    # Dados da área do agente
    area_data = {
        'nome': agente.area_nome,
        'coordenadas': agente.area_coordenadas,
    }
    
    # Outros agentes (para mostrar áreas vizinhas)
    outros_agentes = AgenteSaude.objects.exclude(id=agente.id)
    outros_agentes_data = []
    for a in outros_agentes:
        outros_agentes_data.append({
            'nome': a.usuario.get_full_name(),
            'area_nome': a.area_nome,
            'coordenadas': a.area_coordenadas,
            'username': a.usuario.username,
        })
    
    return JsonResponse({
        'pacientes': pacientes_data,
        'residencias': residencias_data,
        'minha_area': area_data,
        'outras_areas': outros_agentes_data,
    })


@login_required
def mapa_dados_medico(request):
    """API endpoint para dados do mapa - visão do médico (acesso completo)"""
    if request.user.tipo != 'MEDICO':
        return JsonResponse({'error': 'Acesso negado'}, status=403)
    
    # Buscar todos os pacientes
    pacientes = Paciente.objects.all().select_related('residencia', 'agente')
    
    pacientes_data = []
    for p in pacientes:
        pacientes_data.append({
            'id': p.id,
            'nome': p.nome,
            'idade': p.idade,
            'is_infantil': p.is_infantil,
            'cpf': p.cpf,
            'tipo_sanguineo': p.tipo_sanguineo,
            'endereco': p.endereco,
            'bairro': p.bairro,
            'latitude': float(p.latitude) if p.latitude else None,
            'longitude': float(p.longitude) if p.longitude else None,
            'residencia_id': p.residencia.id if p.residencia else None,
            'doenca_atual': p.doenca_atual,
            'nivel_gravidade': p.nivel_gravidade,
            'is_cronica': p.is_cronica,
            'is_contagiosa': p.is_contagiosa,
            'medicamentos': p.medicamentos,
            'medicamentos_prescritos': p.medicamentos_prescritos,
            'necessidades_basicas': p.necessidades_basicas,
            'recebe_auxilio_governo': p.recebe_auxilio_governo,
            'tipo_auxilio': p.tipo_auxilio,
            'tem_acamado': p.tem_acamado,
            'ultima_consulta': p.ultima_consulta.strftime('%d/%m/%Y') if p.ultima_consulta else None,
            'proxima_consulta': p.proxima_consulta.strftime('%d/%m/%Y') if p.proxima_consulta else None,
            'comorbidade': p.comorbidade,
            'comorbidade_tipo': p.comorbidade_tipo,
            'teve_avc': p.teve_avc,
            'teve_infarto': p.teve_infarto,
            'bebe': p.bebe,
            'tipo_bebida': p.tipo_bebida,
            'fuma': p.fuma,
            'cigarros_por_dia': p.cigarros_por_dia,
            'alergia': p.alergia,
            'alergia_tipo': p.alergia_tipo,
            # Dados sigilosos - apenas para médicos
            'prontuario_completo': p.prontuario_completo,
            'agente': p.agente.usuario.get_full_name() if p.agente else 'Não atribuído',
        })
    
    # Buscar todas as residências
    residencias = Residencia.objects.all()
    
    residencias_data = []
    for r in residencias:
        residencias_data.append({
            'id': r.id,
            'endereco': f'{r.endereco_completo}, {r.numero}',
            'bairro': r.bairro,
            'status': r.status,
            'status_display': r.get_status_display(),
            'qtd_moradores': r.qtd_moradores,
            'latitude': float(r.latitude),
            'longitude': float(r.longitude),
            'cadastrada': r.status == 'CADASTRADA',
        })
    
    # Todas as áreas dos agentes
    agentes = AgenteSaude.objects.all()
    areas_agentes = []
    for a in agentes:
        areas_agentes.append({
            'nome': a.usuario.get_full_name(),
            'area_nome': a.area_nome,
            'coordenadas': a.area_coordenadas,
            'username': a.usuario.username,
        })
    
    return JsonResponse({
        'pacientes': pacientes_data,
        'residencias': residencias_data,
        'areas_agentes': areas_agentes,
    })


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
