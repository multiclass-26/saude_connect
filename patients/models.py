from django.db import models
from accounts.models import Usuario, AgenteSaude

class Residencia(models.Model):
    STATUS_CHOICES = [
        ('CADASTRADA', 'Cadastrada'),
        ('NAO_CADASTRADA', 'Não Cadastrada'),
        ('PENDENTE', 'Pendente'),
    ]
    
    agente = models.ForeignKey(AgenteSaude, on_delete=models.SET_NULL, null=True, blank=True, related_name='residencias')
    endereco_completo = models.CharField(max_length=300)
    cidade = models.CharField(max_length=100, default='Aracaju')
    bairro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NAO_CADASTRADA')
    qtd_moradores = models.IntegerField('Quantidade de Moradores', default=0)
    
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Residência'
        verbose_name_plural = 'Residências'
        ordering = ['bairro', 'endereco_completo']
    
    def __str__(self):
        return f"{self.endereco_completo}, {self.numero} - {self.bairro}"


class Paciente(models.Model):
    TIPO_SANGUINEO_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    GRAVIDADE_CHOICES = [
        ('LEVE', 'Leve'),
        ('MODERADA', 'Moderada'),
        ('GRAVE', 'Grave'),
        ('CRITICA', 'Crítica'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente_perfil')
    agente = models.ForeignKey(AgenteSaude, on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes')
    residencia = models.ForeignKey(Residencia, on_delete=models.SET_NULL, null=True, blank=True, related_name='moradores')
    
    foto = models.ImageField(upload_to='pacientes/', blank=True, null=True)
    nome = models.CharField(max_length=200)
    idade = models.IntegerField()
    is_infantil = models.BooleanField('É criança/adolescente', default=False)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    tipo_sanguineo = models.CharField('Tipo Sanguíneo', max_length=3, choices=TIPO_SANGUINEO_CHOICES, blank=True)
    pessoas_na_casa = models.IntegerField('Qtd. pessoas na casa', null=True, blank=True)
    
    # Localização
    cidade = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    endereco = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Condições de saúde
    comorbidade = models.BooleanField(default=False)
    comorbidade_tipo = models.TextField(blank=True)
    teve_avc = models.BooleanField('Teve AVC', default=False)
    teve_infarto = models.BooleanField('Teve Infarto', default=False)
    
    # Doença atual
    doenca_atual = models.CharField('Doença ou Infecção Atual', max_length=200, blank=True)
    nivel_gravidade = models.CharField('Nível de Gravidade', max_length=10, choices=GRAVIDADE_CHOICES, blank=True)
    is_cronica = models.BooleanField('É doença crônica', default=False)
    is_contagiosa = models.BooleanField('É contagiosa', default=False)
    
    # Hábitos
    bebe = models.BooleanField('Bebe álcool', default=False)
    tipo_bebida = models.CharField(max_length=100, blank=True)
    
    fuma = models.BooleanField(default=False)
    cigarros_por_dia = models.IntegerField(default=0)
    anos_fumando = models.IntegerField(default=0)
    
    # Medicamentos
    medicamentos = models.TextField('Medicamentos em uso', blank=True)
    medicamentos_prescritos = models.BooleanField('Necessita prescrição médica', default=False)
    
    # Necessidades
    necessidades_basicas = models.TextField('Necessidades Básicas (fraldas, visita domiciliar, etc)', blank=True)
    recebe_auxilio_governo = models.BooleanField('Recebe auxílio do governo', default=False)
    tipo_auxilio = models.CharField('Tipo de auxílio', max_length=200, blank=True)
    tem_acamado = models.BooleanField('Tem alguém acamado', default=False)
    
    # Saúde geral
    alergia = models.BooleanField('Possui alergia', default=False)
    alergia_tipo = models.TextField('Tipo de alergia', blank=True)
    
    atividade_fisica = models.BooleanField('Pratica atividade física', default=False)
    atividade_tipo = models.CharField('Tipo de exercício', max_length=200, blank=True)
    atividade_frequencia = models.CharField('Frequência', max_length=100, blank=True)
    
    # Acompanhamento
    ultima_consulta = models.DateField('Última Consulta', null=True, blank=True)
    proxima_consulta = models.DateField('Próxima Consulta Agendada', null=True, blank=True)
    
    # Prontuário (dados sigilosos - apenas médicos)
    prontuario_completo = models.TextField('Prontuário Completo', blank=True, help_text='Informações sigilosas')
    
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
