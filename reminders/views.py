from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Alarme

@login_required
def dashboard_paciente(request):
    if request.user.tipo != 'PACIENTE':
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')
    
    return render(request, 'reminders/dashboard_paciente.html')

@login_required
def lembretes_view(request):
    if request.user.tipo != 'PACIENTE':
        messages.error(request, 'Acesso negado.')
        return redirect('dashboard')
    
    alarmes = Alarme.objects.filter(paciente=request.user, ativo=True)
    
    if request.method == 'POST':
        try:
            medicamento = request.POST.get('medicamento')
            data_hora = request.POST.get('data_hora')
            
            Alarme.objects.create(
                paciente=request.user,
                medicamento=medicamento,
                data_hora=data_hora
            )
            messages.success(request, 'Lembrete criado com sucesso!')
            return redirect('lembretes')
        except Exception as e:
            messages.error(request, f'Erro ao criar lembrete: {str(e)}')
    
    return render(request, 'reminders/lembretes.html', {'alarmes': alarmes})

@login_required
def excluir_alarme(request, pk):
    if request.user.tipo != 'PACIENTE':
        return JsonResponse({'success': False, 'error': 'Acesso negado'})
    
    try:
        alarme = Alarme.objects.get(pk=pk, paciente=request.user)
        alarme.delete()
        return JsonResponse({'success': True})
    except Alarme.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alarme não encontrado'})

@login_required
def verificar_alarmes(request):
    if request.user.tipo != 'PACIENTE':
        return JsonResponse({'alarmes': []})
    
    now = timezone.now()
    alarmes_vencidos = Alarme.objects.filter(
        paciente=request.user,
        ativo=True,
        notificado=False,
        data_hora__lte=now
    )
    
    dados_alarmes = []
    for alarme in alarmes_vencidos:
        dados_alarmes.append({
            'id': alarme.id,
            'medicamento': alarme.medicamento,
            'data_hora': alarme.data_hora.strftime('%d/%m/%Y %H:%M')
        })
        alarme.notificado = True
        alarme.ativo = False
        alarme.save()
    
    return JsonResponse({'alarmes': dados_alarmes})
