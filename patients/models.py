from django.db import models
from accounts.models import Usuario, AgenteSaude

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente_perfil')
    agente = models.ForeignKey(AgenteSaude, on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes')
    
    foto = models.ImageField(upload_to='pacientes/', blank=True, null=True)
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    pessoas_na_casa = models.IntegerField('Qtd. pessoas na casa', null=True, blank=True)
    
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    endereco = models.TextField()
    
    comorbidade = models.BooleanField(default=False)
    comorbidade_tipo = models.TextField(blank=True)
    teve_avc = models.BooleanField('Teve AVC', default=False)
    teve_infarto = models.BooleanField('Teve Infarto', default=False)
    
    bebe = models.BooleanField('Bebe álcool', default=False)
    tipo_bebida = models.CharField(max_length=100, blank=True)
    
    fuma = models.BooleanField(default=False)
    cigarros_por_dia = models.IntegerField(default=0)
    anos_fumando = models.IntegerField(default=0)
    
    medicamentos = models.TextField('Medicamentos em uso', blank=True)
    
    alergia = models.BooleanField('Possui alergia', default=False)
    alergia_tipo = models.TextField('Tipo de alergia', blank=True)
    
    atividade_fisica = models.BooleanField('Pratica atividade física', default=False)
    atividade_tipo = models.CharField('Tipo de exercício', max_length=200, blank=True)
    atividade_frequencia = models.CharField('Frequência', max_length=100, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    @property
    def carga_tabagica(self):
        if self.fuma and self.cigarros_por_dia and self.anos_fumando:
            return (self.cigarros_por_dia / 20) * self.anos_fumando
        return 0
    
    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"{self.nome} - {self.cpf or 'Sem CPF'}"
