from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('MEDICO', 'Médico'),
        ('AGENTE', 'Agente de Saúde'),
        ('PACIENTE', 'Paciente'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_tipo_display()})"


class Medico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='medico')
    crm = models.CharField('CRM', max_length=20, unique=True)
    
    class Meta:
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'
    
    def __str__(self):
        return f"Dr(a). {self.usuario.get_full_name()} - CRM: {self.crm}"


class AgenteSaude(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='agente')
    id_agente = models.CharField('ID do Agente', max_length=20, unique=True)
    
    class Meta:
        verbose_name = 'Agente de Saúde'
        verbose_name_plural = 'Agentes de Saúde'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - ID: {self.id_agente}"
