"""
Script para popular o banco com MAIS dados fictícios para uma apresentação melhor
"""
import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import AgenteSaude
from patients.models import Residencia, Paciente

def criar_populacao_maior():
    print('🏠 Criando população maior de dados para apresentação...\n')
    
    # Buscar agentes
    try:
        paulo = AgenteSaude.objects.get(usuario__username='agente')
        andre = AgenteSaude.objects.get(usuario__username='andre_agente')
        fernanda = AgenteSaude.objects.get(usuario__username='fernanda_agente')
    except AgenteSaude.DoesNotExist:
        print('❌ Erro: Execute primeiro: python configurar_areas_agentes.py')
        return
    
    # Dados fictícios expandidos
    nomes_masculinos = [
        'João', 'José', 'Antonio', 'Francisco', 'Carlos', 'Paulo', 'Pedro', 'Lucas', 'Marcos', 'Felipe',
        'Bruno', 'Rafael', 'Daniel', 'Rodrigo', 'Gabriel', 'Leonardo', 'Eduardo', 'Fernando', 'Gustavo', 'Thiago',
        'Ricardo', 'Henrique', 'Diego', 'Roberto', 'Marcelo', 'André', 'Vinícius', 'Leandro', 'Fábio', 'Márcio'
    ]
    
    nomes_femininos = [
        'Maria', 'Ana', 'Francisca', 'Antônia', 'Adriana', 'Juliana', 'Márcia', 'Fernanda', 'Patricia', 'Aline',
        'Sandra', 'Camila', 'Amanda', 'Tatiana', 'Renata', 'Vanessa', 'Simone', 'Monica', 'Cristina', 'Luciana',
        'Daniela', 'Claudia', 'Beatriz', 'Carolina', 'Larissa', 'Priscila', 'Gabriela', 'Letícia', 'Roberta', 'Carla'
    ]
    
    sobrenomes = [
        'Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes',
        'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Almeida', 'Lopes', 'Soares', 'Fernandes', 'Vieira', 'Barbosa',
        'Rocha', 'Dias', 'Nascimento', 'Monteiro', 'Mendes', 'Cardoso', 'Araújo', 'Castro', 'Pinto', 'Freitas'
    ]
    
    tipos_sanguineos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    
    doencas = [
        'Hipertensão arterial', 'Diabetes tipo 2', 'Diabetes tipo 1', 'Asma', 'Bronquite crônica', 
        'Artrite reumatoide', 'Depressão', 'Ansiedade', 'Insuficiência cardíaca', 'Arritmia cardíaca',
        'DPOC', 'Osteoporose', 'Gastrite', 'Rinite alérgica', 'Sinusite crônica', 'Enxaqueca',
        'Hipotireoidismo', 'Fibromialgia', 'Artrose', 'Colesterol alto', 'Anemia', 'Obesidade'
    ]
    
    medicamentos_comuns = [
        'Losartana 50mg - 1 comp. ao dia',
        'Metformina 850mg - 1 comp. 2x ao dia',
        'Sinvastatina 20mg - 1 comp. à noite',
        'AAS 100mg - 1 comp. ao dia',
        'Enalapril 10mg - 1 comp. 2x ao dia',
        'Omeprazol 20mg - 1 comp. em jejum',
        'Levotiroxina 50mcg - 1 comp. em jejum',
        'Paracetamol 750mg - SOS dor',
        'Dipirona 500mg - SOS dor/febre',
        'Salbutamol spray - 2 jatos SOS',
        'Captopril 25mg - 1 comp. 2x ao dia',
        'Hidroclorotiazida 25mg - 1 comp. ao dia',
        'Glibenclamida 5mg - 1 comp. antes do café',
        'Amitriptilina 25mg - 1 comp. à noite',
        'Fluoxetina 20mg - 1 comp. pela manhã'
    ]
    
    necessidades = [
        'Fraldas geriátricas', 'Visita domiciliar semanal', 'Cadeira de rodas',
        'Medicação controlada', 'Acompanhamento nutricional', 'Fisioterapia domiciliar',
        'Fraldas infantis', 'Leite especial', 'Suporte psicológico',
        'Auxílio para banho', 'Cama hospitalar', 'Oxigênio domiciliar',
        'Curativos regulares', 'Aferição de glicemia', 'Controle de pressão'
    ]
    
    auxilios = ['Bolsa Família', 'BPC - Benefício de Prestação Continuada', 'Auxílio Brasil', 'Aposentadoria', 'Pensão']
    
    # Áreas de cada agente
    areas_agentes = {
        paulo: {
            'bairros': ['Centro', 'São José'],
            'coordenadas_base': [-10.9445, -37.0705],
            'ruas': [
                'Rua das Flores', 'Av. Beira Mar', 'Rua João Pessoa', 'Rua Laranjeiras', 'Rua Pacatuba',
                'Rua General Jardim', 'Rua Itabaianinha', 'Av. Rio Branco', 'Rua Maruim', 'Rua Lagarto',
                'Rua Santo Amaro', 'Rua São Francisco', 'Rua Itabaiana', 'Praça Camerino', 'Rua Aurora'
            ]
        },
        andre: {
            'bairros': ['Jardins', 'Treze de Julho', 'Salgado Filho'],
            'coordenadas_base': [-10.9495, -37.0705],
            'ruas': [
                'Rua Itabaiana', 'Av. Hermes Fontes', 'Rua São Cristóvão', 'Rua Propriá', 'Av. Ivo do Prado',
                'Rua Estância', 'Rua Simão Dias', 'Av. Beira Mar', 'Rua Tobias Barreto', 'Rua Aracaju',
                'Rua Vila Nova', 'Rua Arauá', 'Rua Cedro', 'Av. Augusto Franco', 'Rua Japaratuba'
            ]
        },
        fernanda: {
            'bairros': ['Bugio', 'Ponto Novo', 'Getúlio Vargas'],
            'coordenadas_base': [-10.9445, -37.0755],
            'ruas': [
                'Rua Campos', 'Rua Estância', 'Rua Simão Dias', 'Av. Tancredo Neves', 'Rua Divina Pastora',
                'Rua Porto da Folha', 'Rua Riachão', 'Rua Carira', 'Rua Frei Paulo', 'Av. Barão de Maruim',
                'Rua Cristinápolis', 'Rua Nossa Senhora Aparecida', 'Rua Neópolis', 'Rua Poço Verde', 'Rua Malhador'
            ]
        }
    }
    
    contador_pacientes = 0
    contador_residencias = 0
    
    for agente, dados_area in areas_agentes.items():
        print(f'\n📍 Criando dados para {agente.usuario.get_full_name()}...')
        
        # Criar 20-25 residências por agente (MAIS QUE ANTES)
        num_residencias = random.randint(20, 25)
        
        for i in range(num_residencias):
            # Coordenadas aleatórias na área do agente
            lat_base, lng_base = dados_area['coordenadas_base']
            lat = lat_base + random.uniform(-0.0045, 0.0045)
            lng = lng_base + random.uniform(-0.0045, 0.0045)
            
            bairro = random.choice(dados_area['bairros'])
            rua = random.choice(dados_area['ruas'])
            numero = random.randint(10, 999)
            
            # Mais residências cadastradas
            status = random.choices(
                ['CADASTRADA', 'NAO_CADASTRADA', 'PENDENTE'],
                weights=[75, 15, 10]
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
                qtd_moradores=random.randint(1, 6) if status == 'CADASTRADA' else 0
            )
            
            contador_residencias += 1
            
            # Se cadastrada, criar pacientes
            if status == 'CADASTRADA':
                num_pacientes = random.randint(1, 5)  # Até 5 por residência
                
                for j in range(num_pacientes):
                    idade = random.randint(0, 92)
                    is_infantil = idade < 18
                    genero = random.choice(['M', 'F'])
                    
                    # Nome completo
                    if genero == 'M':
                        primeiro_nome = random.choice(nomes_masculinos)
                    else:
                        primeiro_nome = random.choice(nomes_femininos)
                    
                    sobrenome = random.choice(sobrenomes)
                    nome_completo = f'{primeiro_nome} {sobrenome}'
                    
                    # CPF fictício
                    cpf = f'{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}'
                    
                    # Doença baseada na idade
                    tem_doenca = False
                    doenca_atual = ''
                    gravidade = ''
                    
                    if idade > 60:
                        tem_doenca = random.random() < 0.7  # 70% chance
                    elif idade > 40:
                        tem_doenca = random.random() < 0.4  # 40% chance
                    elif is_infantil:
                        tem_doenca = random.random() < 0.15  # 15% chance
                    else:
                        tem_doenca = random.random() < 0.25  # 25% chance
                    
                    if tem_doenca:
                        doenca_atual = random.choice(doencas)
                        
                        if any(d in doenca_atual for d in ['Insuficiência', 'DPOC', 'cardíaca']):
                            gravidade = random.choice(['GRAVE', 'CRITICA'])
                        elif any(d in doenca_atual for d in ['Diabetes', 'Hipertensão']):
                            gravidade = random.choice(['MODERADA', 'GRAVE'])
                        else:
                            gravidade = random.choice(['LEVE', 'MODERADA'])
                    
                    # Medicamentos
                    if tem_doenca:
                        num_meds = random.randint(1, 4)
                        meds = random.sample(medicamentos_comuns, min(num_meds, len(medicamentos_comuns)))
                        medicamentos_texto = '\n'.join(meds)
                        precisa_prescricao = True
                    else:
                        medicamentos_texto = ''
                        precisa_prescricao = False
                    
                    # Necessidades especiais
                    tem_necessidades = False
                    if idade > 75:
                        tem_necessidades = random.random() < 0.5
                    elif is_infantil and idade < 3:
                        tem_necessidades = random.random() < 0.3
                    
                    necessidades_texto = random.choice(necessidades) if tem_necessidades else ''
                    
                    # Auxílio governo
                    recebe_auxilio = False
                    tipo_auxilio_texto = ''
                    if idade > 65:
                        recebe_auxilio = random.random() < 0.6
                        tipo_auxilio_texto = random.choice(['Aposentadoria', 'BPC']) if recebe_auxilio else ''
                    elif idade < 18:
                        recebe_auxilio = random.random() < 0.3
                        tipo_auxilio_texto = random.choice(['Bolsa Família', 'Auxílio Brasil']) if recebe_auxilio else ''
                    else:
                        recebe_auxilio = random.random() < 0.2
                        tipo_auxilio_texto = random.choice(auxilios) if recebe_auxilio else ''
                    
                    # Última consulta
                    dias_atras = random.randint(5, 730)
                    ultima_consulta = date.today() - timedelta(days=dias_atras)
                    
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
                        comorbidade=random.choice([True, False]) if idade > 50 else False,
                        comorbidade_tipo='Hipertensão e Diabetes' if idade > 60 and random.choice([True, False]) else '',
                        teve_avc=random.choice([True, False]) if idade > 65 else False,
                        teve_infarto=random.choice([True, False]) if idade > 65 else False,
                        
                        # Doença atual
                        doenca_atual=doenca_atual,
                        nivel_gravidade=gravidade,
                        is_cronica=random.choice([True, False]) if tem_doenca else False,
                        is_contagiosa=random.choice([True, False]) if 'Rinite' not in doenca_atual and tem_doenca else False,
                        
                        # Hábitos
                        bebe=random.choice([True, False]) if idade > 18 else False,
                        tipo_bebida=random.choice(['Cerveja', 'Vinho', 'Destilados']) if idade > 18 and random.random() < 0.3 else '',
                        fuma=random.choice([True, False]) if idade > 18 else False,
                        cigarros_por_dia=random.randint(5, 20) if idade > 18 and random.random() < 0.2 else 0,
                        anos_fumando=random.randint(5, 40) if idade > 18 and random.random() < 0.2 else 0,
                        
                        # Medicamentos
                        medicamentos=medicamentos_texto,
                        medicamentos_prescritos=precisa_prescricao,
                        
                        # Necessidades
                        necessidades_basicas=necessidades_texto,
                        recebe_auxilio_governo=recebe_auxilio,
                        tipo_auxilio=tipo_auxilio_texto,
                        tem_acamado=random.choice([True, False]) if idade > 80 else False,
                        
                        # Saúde
                        alergia=random.choice([True, False]),
                        alergia_tipo=random.choice(['Poeira', 'Lactose', 'Glúten', 'Medicamentos', 'Pólen']) if random.random() < 0.2 else '',
                        atividade_fisica=random.choice([True, False]) if idade > 18 and idade < 70 else False,
                        atividade_tipo=random.choice(['Caminhada', 'Academia', 'Natação', 'Ciclismo', 'Corrida']) if random.random() < 0.3 else '',
                        atividade_frequencia=random.choice(['3x semana', 'Diariamente', '2x semana', '5x semana']) if random.random() < 0.3 else '',
                        
                        # Consultas
                        ultima_consulta=ultima_consulta,
                        proxima_consulta=date.today() + timedelta(days=random.randint(30, 180)) if tem_doenca else None,
                        
                        # Prontuário sigiloso
                        prontuario_completo=f'Paciente em acompanhamento desde {ultima_consulta.strftime("%d/%m/%Y")}. {doenca_atual if doenca_atual else "Saúde estável"}. {random.choice(["Boa adesão ao tratamento", "Necessita reforço educativo", "Família colaborativa", "Dificuldade financeira", "Resistente a orientações", "Excelente evolução"])}'
                    )
                    
                    contador_pacientes += 1
            
            if (i+1) % 5 == 0:
                print(f'  ✓ {i+1}/{num_residencias} residências criadas...')
    
    print(f'\n✅ População expandida criada com sucesso!')
    print(f'   📊 Total de residências: {contador_residencias}')
    print(f'   👥 Total de pacientes: {contador_pacientes}')
    print(f'\n🎯 Distribuição por agente:')
    print(f'   • Paulo: {Paciente.objects.filter(agente__usuario__username="agente").count()} pacientes')
    print(f'   • André: {Paciente.objects.filter(agente__usuario__username="andre_agente").count()} pacientes')
    print(f'   • Fernanda: {Paciente.objects.filter(agente__usuario__username="fernanda_agente").count()} pacientes')
    
    # Estatísticas adicionais
    print(f'\n📈 Estatísticas:')
    print(f'   • Casos graves: {Paciente.objects.filter(nivel_gravidade__in=["GRAVE", "CRITICA"]).count()}')
    print(f'   • Doenças crônicas: {Paciente.objects.filter(is_cronica=True).count()}')
    print(f'   • Crianças/adolescentes: {Paciente.objects.filter(is_infantil=True).count()}')
    print(f'   • Recebem auxílio governo: {Paciente.objects.filter(recebe_auxilio_governo=True).count()}')

if __name__ == '__main__':
    resposta = input('\n⚠️  Deseja LIMPAR dados antigos antes? (s/N): ')
    if resposta.lower() == 's':
        Paciente.objects.all().delete()
        Residencia.objects.all().delete()
        print('✓ Dados antigos removidos.\n')
    
    criar_populacao_maior()
