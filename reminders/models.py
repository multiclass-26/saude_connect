from django.db import models
from accounts.models import Usuario

class Alarme(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='alarmes')
    medicamento = models.CharField(max_length=200)
    data_hora = models.DateTimeField()
    ativo = models.BooleanField(default=True)
    notificado = models.BooleanField(default=False)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Alarme'
        verbose_name_plural = 'Alarmes'
        ordering = ['data_hora']
    
    def __str__(self):
        return f"{self.medicamento} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
