"""
Script para popular o banco de dados com residências e pacientes fictícios
para demonstração no simpósio.
"""
import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import AgenteSaude
from patients.models import Residencia, Paciente

def criar_residencias_e_pacientes():
    print('🏠 Populando banco de dados com residências e pacientes...\n')
    
    # Buscar agentes
    try:
        # Buscar por username ao invés de id_agente
        paulo = AgenteSaude.objects.get(usuario__username='agente')
        andre = AgenteSaude.objects.get(usuario__username='andre_agente')
        fernanda = AgenteSaude.objects.get(usuario__username='fernanda_agente')
    except AgenteSaude.DoesNotExist:
        print('❌ Erro: Execute primeiro: python configurar_areas_agentes.py')
        return
    
    # Dados fictícios
    nomes = [
        'Maria Silva', 'João Santos', 'Ana Costa', 'Pedro Oliveira', 'Carla Mendes',
        'Roberto Lima', 'Juliana Rocha', 'Francisco Alves', 'Fernanda Souza', 'Carlos Pereira',
        'Beatriz Martins', 'Lucas Fernandes', 'Patrícia Gomes', 'Ricardo Almeida', 'Cristina Barros',
        'Felipe Cardoso', 'Amanda Ribeiro', 'Gustavo Araújo', 'Mariana Teixeira', 'Eduardo Pinto',
        'Isabela Moura', 'Rafael Dias', 'Camila Nascimento', 'Thiago Monteiro', 'Vanessa Castro'
    ]
    
    sobrenomes = ['da Silva', 'Santos', 'Costa', 'Oliveira', 'Souza', 'Lima', 'Ferreira', 'Alves', 'Pereira', 'Rodrigues']
    
    tipos_sanguineos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    
    doencas = [
        'Hipertensão arterial', 'Diabetes tipo 2', 'Asma', 'Bronquite crônica', 
        'Artrite reumatoide', 'Depressão', 'Ansiedade', 'Insuficiência cardíaca',
        'DPOC', 'Osteoporose', 'Gastrite', 'Rinite alérgica'
    ]
    
    medicamentos_comuns = [
        'Losartana 50mg (1x ao dia)', 'Metformina 850mg (2x ao dia)', 
        'Sinvastatina 20mg (1x ao dia - noite)', 'AAS 100mg (1x ao dia)',
        'Enalapril 10mg (2x ao dia)', 'Omeprazol 20mg (1x ao dia - jejum)',
        'Paracetamol 750mg (conforme necessário)', 'Dipirona 500mg (SOS)',
        'Salbutamol spray (SOS)', 'Captopril 25mg (2x ao dia)'
    ]
    
    necessidades = [
        'Fraldas geriátricas', 'Visita domiciliar semanal', 'Cadeira de rodas',
        'Medicação controlada', 'Acompanhamento nutricional', 'Fisioterapia',
        'Fraldas infantis', 'Leite especial', 'Suporte psicológico'
    ]
    
    auxilios = ['Bolsa Família', 'BPC - Benefício de Prestação Continuada', 'Auxílio Brasil', 'Aposentadoria']
    
    # Áreas de cada agente
    areas_agentes = {
        paulo: {
            'bairros': ['Centro', 'São José'],
            'coordenadas_base': [-10.9445, -37.0705],
            'ruas': ['Rua das Flores', 'Av. Beira Mar', 'Rua João Pessoa', 'Rua Laranjeiras', 'Rua Pacatuba']
        },
        andre: {
            'bairros': ['Jardins', 'Treze de Julho'],
            'coordenadas_base': [-10.9495, -37.0705],
            'ruas': ['Rua Itabaiana', 'Av. Hermes Fontes', 'Rua São Cristóvão', 'Rua Propriá', 'Av. Ivo do Prado']
        },
        fernanda: {
            'bairros': ['Bugio', 'Ponto Novo'],
            'coordenadas_base': [-10.9445, -37.0755],
            'ruas': ['Rua Campos', 'Rua Estância', 'Rua Simão Dias', 'Av. Tancredo Neves', 'Rua Divina Pastora']
        }
    }
    
    contador_pacientes = 0
    contador_residencias = 0
    
    for agente, dados_area in areas_agentes.items():
        print(f'\n📍 Criando dados para {agente.usuario.get_full_name()} ({dados_area["bairros"][0]})...')
        
        # Criar 8-10 residências por agente
        num_residencias = random.randint(8, 10)
        
        for i in range(num_residencias):
            # Coordenadas aleatórias na área do agente
            lat_base, lng_base = dados_area['coordenadas_base']
            lat = lat_base + random.uniform(-0.003, 0.003)
            lng = lng_base + random.uniform(-0.003, 0.003)
            
            bairro = random.choice(dados_area['bairros'])
            rua = random.choice(dados_area['ruas'])
            numero = random.randint(10, 999)
            
            # Algumas residências não cadastradas
            status = random.choices(
                ['CADASTRADA', 'NAO_CADASTRADA', 'PENDENTE'],
                weights=[70, 20, 10]
            )[0]
            
            residencia = Residencia.objects.create(
                agente=agente if status != 'NAO_CADASTRADA' else None,
                endereco_completo=f'{rua}',
                cidade='Aracaju',
                bairro=bairro,
                numero=str(numero),
                latitude=lat,
                longitude=lng,
                status=status,
                qtd_moradores=random.randint(1, 5) if status == 'CADASTRADA' else 0
            )
            
            contador_residencias += 1
            
            # Se cadastrada, criar pacientes
            if status == 'CADASTRADA':
                num_pacientes = random.randint(1, 4)
                
                for j in range(num_pacientes):
                    idade = random.randint(1, 85)
                    is_infantil = idade < 18
                    
                    # Gerar CPF fictício
                    cpf = f'{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}'
                    
                    # Escolher se tem doença
                    tem_doenca = random.choice([True, False])
                    doenca_atual = random.choice(doencas) if tem_doenca else ''
                    
                    # Gravidade baseada na doença
                    if tem_doenca:
                        if any(d in doenca_atual for d in ['Insuficiência', 'DPOC', 'cardíaca']):
                            gravidade = random.choice(['GRAVE', 'CRITICA'])
                        elif any(d in doenca_atual for d in ['Diabetes', 'Hipertensão']):
                            gravidade = random.choice(['MODERADA', 'GRAVE'])
                        else:
                            gravidade = random.choice(['LEVE', 'MODERADA'])
                    else:
                        gravidade = ''
                    
                    # Medicamentos
                    if tem_doenca:
                        num_meds = random.randint(1, 3)
                        meds = random.sample(medicamentos_comuns, num_meds)
                        medicamentos_texto = '\n'.join(meds)
                        precisa_prescricao = True
                    else:
                        medicamentos_texto = ''
                        precisa_prescricao = False
                    
                    # Necessidades especiais
                    tem_necessidades = random.choice([True, False]) if idade > 60 or is_infantil else False
                    necessidades_texto = random.choice(necessidades) if tem_necessidades else ''
                    
                    # Auxílio governo
                    recebe_auxilio = random.choice([True, False])
                    tipo_auxilio_texto = random.choice(auxilios) if recebe_auxilio else ''
                    
                    # Última consulta
                    dias_atras = random.randint(10, 365)
                    ultima_consulta = date.today() - timedelta(days=dias_atras)
                    
                    # Nome fictício
                    nome_completo = nomes[contador_pacientes % len(nomes)]
                    
                    paciente = Paciente.objects.create(
                        agente=agente,
                        residencia=residencia,
                        nome=nome_completo,
                        idade=idade,
                        is_infantil=is_infantil,
                        peso=round(random.uniform(3.5 if is_infantil else 45, 50 if is_infantil else 120), 1),
                        cpf=cpf,
                        tipo_sanguineo=random.choice(tipos_sanguineos),
                        pessoas_na_casa=residencia.qtd_moradores,
                        cidade='Aracaju',
                        bairro=bairro,
                        endereco=f'{rua}, {numero}',
                        latitude=lat,
                        longitude=lng,
                        
                        # Comorbidades
                        comorbidade=random.choice([True, False]) if idade > 40 else False,
                        comorbidade_tipo='Hipertensão, Diabetes' if idade > 50 and random.choice([True, False]) else '',
                        teve_avc=random.choice([True, False]) if idade > 60 else False,
                        teve_infarto=random.choice([True, False]) if idade > 60 else False,
                        
                        # Doença atual
                        doenca_atual=doenca_atual,
                        nivel_gravidade=gravidade,
                        is_cronica=random.choice([True, False]) if tem_doenca else False,
                        is_contagiosa=random.choice([True, False]) if 'Rinite' not in doenca_atual and tem_doenca else False,
                        
                        # Hábitos
                        bebe=random.choice([True, False]) if idade > 18 else False,
                        tipo_bebida=random.choice(['Cerveja', 'Vinho', 'Destilados']) if idade > 18 and random.choice([True, False]) else '',
                        fuma=random.choice([True, False]) if idade > 18 else False,
                        cigarros_por_dia=random.randint(5, 20) if idade > 18 and random.choice([True, False]) else 0,
                        anos_fumando=random.randint(5, 30) if idade > 18 and random.choice([True, False]) else 0,
                        
                        # Medicamentos
                        medicamentos=medicamentos_texto,
                        medicamentos_prescritos=precisa_prescricao,
                        
                        # Necessidades
                        necessidades_basicas=necessidades_texto,
                        recebe_auxilio_governo=recebe_auxilio,
                        tipo_auxilio=tipo_auxilio_texto,
                        tem_acamado=random.choice([True, False]) if idade > 70 else False,
                        
                        # Saúde
                        alergia=random.choice([True, False]),
                        alergia_tipo=random.choice(['Poeira', 'Lactose', 'Glúten', 'Medicamentos']) if random.choice([True, False]) else '',
                        atividade_fisica=random.choice([True, False]),
                        atividade_tipo=random.choice(['Caminhada', 'Academia', 'Natação', 'Ciclismo']) if random.choice([True, False]) else '',
                        atividade_frequencia=random.choice(['3x semana', 'Diariamente', '2x semana']) if random.choice([True, False]) else '',
                        
                        # Consultas
                        ultima_consulta=ultima_consulta,
                        proxima_consulta=date.today() + timedelta(days=random.randint(30, 90)) if tem_doenca else None,
                        
                        # Prontuário sigiloso
                        prontuario_completo=f'Paciente sob acompanhamento desde {ultima_consulta}. Histórico de {doenca_atual if doenca_atual else "saúde estável"}. Observações: {random.choice(["Boa adesão ao tratamento", "Necessita reforço educativo", "Família colaborativa", "Dificuldade financeira para medicamentos"])}'
                    )
                    
                    contador_pacientes += 1
                    
                print(f'  ✓ {rua}, {numero} - {status} ({num_pacientes if status == "CADASTRADA" else 0} pacientes)')
    
    print(f'\n✅ Dados criados com sucesso!')
    print(f'   📊 Total de residências: {contador_residencias}')
    print(f'   👥 Total de pacientes: {contador_pacientes}')
    print(f'\n🎯 Distribuição por agente:')
    print(f'   • Paulo: {Paciente.objects.filter(agente__usuario__username="agente").count()} pacientes')
    print(f'   • André: {Paciente.objects.filter(agente__usuario__username="andre_agente").count()} pacientes')
    print(f'   • Fernanda: {Paciente.objects.filter(agente__usuario__username="fernanda_agente").count()} pacientes')

if __name__ == '__main__':
    # Limpar dados antigos (opcional)
    resposta = input('\n⚠️  Deseja limpar dados antigos de pacientes e residências? (s/N): ')
    if resposta.lower() == 's':
        Paciente.objects.all().delete()
        Residencia.objects.all().delete()
        print('✓ Dados antigos removidos.\n')
    
    criar_residencias_e_pacientes()
