"""
View para popular dados do mapa via web (para Railway)
"""
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from accounts.models import AgenteSaude
from patients.models import Paciente, Residencia
import random

@csrf_exempt
def popular_mapa_view(request):
    """Popula dados do mapa - 156 pacientes e 65 residências"""
    
    html = "<html><head><style>"
    html += "body { font-family: Arial; padding: 20px; background: #f5f5f5; }"
    html += "h1 { color: #2c3e50; }"
    html += "h2 { color: #27ae60; margin-top: 30px; }"
    html += ".success { color: #27ae60; }"
    html += ".info { color: #3498db; }"
    html += ".warning { color: #f39c12; }"
    html += ".container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }"
    html += ".stats { display: flex; gap: 20px; margin: 20px 0; }"
    html += ".stat-box { background: #ecf0f1; padding: 15px; border-radius: 5px; flex: 1; }"
    html += ".btn { display: inline-block; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }"
    html += "</style></head><body><div class='container'>"
    html += "<h1>🗺️ Populando Dados do Mapa</h1>"
    
    try:
        # Verificar se agentes existem
        agentes = list(AgenteSaude.objects.all())
        
        if len(agentes) < 3:
            html += "<p class='warning'>⚠️ ATENÇÃO: Configure os agentes primeiro!</p>"
            html += f"<p>Encontrados apenas {len(agentes)} agentes. Necessário 3 agentes configurados.</p>"
            html += "<p><a href='/setup/' class='btn'>Ir para Setup</a></p>"
            html += "</div></body></html>"
            return HttpResponse(html)
        
        paulo = agentes[0]  # agente
        andre = agentes[1]  # andre_agente
        fernanda = agentes[2]  # fernanda_agente
        
        html += f"<p class='info'>✓ Agentes encontrados: {paulo.usuario.first_name}, {andre.usuario.first_name}, {fernanda.usuario.first_name}</p>"
        
        with transaction.atomic():
            # Configurar áreas dos agentes (se não tiverem)
            if not paulo.area_coordenadas:
                paulo.area_nome = "Centro/Salgado Filho/São José"
                paulo.area_coordenadas = [
                    [-10.940, -37.085], [-10.940, -37.060], [-10.955, -37.060], [-10.955, -37.085]
                ]
                paulo.save()
                html += f"<p class='success'>✓ Área configurada para {paulo.usuario.first_name}</p>"
            
            if not andre.area_coordenadas:
                andre.area_nome = "Jardins/Grageru/Treze de Julho"
                andre.area_coordenadas = [
                    [-10.925, -37.065], [-10.925, -37.040], [-10.945, -37.040], [-10.945, -37.065]
                ]
                andre.save()
                html += f"<p class='success'>✓ Área configurada para {andre.usuario.first_name}</p>"
            
            if not fernanda.area_coordenadas:
                fernanda.area_nome = "Farolândia/Inácio Barbosa/Atalaia"
                fernanda.area_coordenadas = [
                    [-10.910, -37.095], [-10.910, -37.070], [-10.930, -37.070], [-10.930, -37.095]
                ]
                fernanda.save()
                html += f"<p class='success'>✓ Área configurada para {fernanda.usuario.first_name}</p>"
            
            # Limpar dados antigos
            Paciente.objects.all().delete()
            Residencia.objects.all().delete()
            html += "<p class='success'>✓ Dados antigos limpos</p>"
            
            # Coordenadas base (Aracaju)
            base_coords = {
                'paulo': {'lat': -10.9472, 'lng': -37.0731},
                'andre': {'lat': -10.9350, 'lng': -37.0550},
                'fernanda': {'lat': -10.9190, 'lng': -37.0850}
            }
            
            # Nomes realistas
            nomes = [
                "Maria Silva", "João Santos", "Ana Costa", "Pedro Oliveira", "Julia Lima",
                "Carlos Mendes", "Patricia Alves", "Roberto Souza", "Fernanda Rocha", "Lucas Barros",
                "Mariana Dias", "Felipe Gomes", "Juliana Martins", "Ricardo Fernandes", "Amanda Rodrigues",
                "Bruno Pereira", "Camila Nascimento", "Daniel Carvalho", "Gabriela Monteiro", "Henrique Ribeiro",
                "Isabel Cardoso", "José Castro", "Laura Moreira", "Miguel Pinto", "Natalia Teixeira"
            ]
            
            ruas = [
                "Rua das Flores", "Av. Presidente Vargas", "Rua São José", "Rua Laranjeiras",
                "Av. Beira Mar", "Rua dos Navegantes", "Rua Pacatuba", "Rua Itabaiana",
                "Av. Tancredo Neves", "Rua Sergipe", "Rua Aracaju", "Rua Propriá",
                "Av. Santos Dumont", "Rua Estância", "Rua Lagarto", "Rua Tobias Barreto"
            ]
            
            bairros_data = [
                ('Centro', paulo, base_coords['paulo']),
                ('Salgado Filho', paulo, base_coords['paulo']),
                ('São José', paulo, base_coords['paulo']),
                ('Jardins', andre, base_coords['andre']),
                ('Grageru', andre, base_coords['andre']),
                ('Treze de Julho', andre, base_coords['andre']),
                ('Farolândia', fernanda, base_coords['fernanda']),
                ('Inácio Barbosa', fernanda, base_coords['fernanda']),
                ('Atalaia', fernanda, base_coords['fernanda'])
            ]
            
            tipos_sanguineos = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            doencas = [
                'Hipertensão Arterial', 'Diabetes Mellitus Tipo 2', 'Asma', 'DPOC',
                'Obesidade', 'Depressão', 'Ansiedade', 'Artrite Reumatoide',
                'Osteoporose', 'Hipotireoidismo', 'Insuficiência Cardíaca', 'AVC prévio'
            ]
            
            medicamentos = [
                'Losartana 50mg', 'Metformina 850mg', 'Sinvastatina 20mg',
                'Omeprazol 20mg', 'AAS 100mg', 'Atenolol 25mg',
                'Captopril 25mg', 'Hidroclorotiazida 25mg', 'Glibenclamida 5mg'
            ]
            
            residencias_criadas = 0
            pacientes_criados = 0
            
            # Criar residências e pacientes por bairro
            for bairro, agente, coords in bairros_data:
                # 7-8 residências por bairro = ~65 total
                num_residencias = random.randint(7, 8)
                
                for i in range(num_residencias):
                    # Coordenadas próximas ao centro do bairro
                    lat = coords['lat'] + random.uniform(-0.01, 0.01)
                    lng = coords['lng'] + random.uniform(-0.01, 0.01)
                    
                    rua = random.choice(ruas)
                    numero = random.randint(10, 999)
                    endereco = f"{rua}, {numero}"
                    
                    # Status da residência
                    status = random.choice(['cadastrada'] * 7 + ['não cadastrada'] * 3)
                    qtd_moradores = random.randint(1, 6)
                    
                    residencia = Residencia.objects.create(
                        endereco=endereco,
                        bairro=bairro,
                        cidade='Aracaju',
                        latitude=lat,
                        longitude=lng,
                        status=status,
                        qtd_moradores=qtd_moradores,
                        agente=agente
                    )
                    residencias_criadas += 1
                    
                    # 2-3 pacientes por residência se cadastrada
                    if status == 'cadastrada':
                        num_pacientes = random.randint(1, 3)
                        
                        for j in range(num_pacientes):
                            nome_base = random.choice(nomes)
                            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
                            
                            idade = random.randint(25, 85)
                            peso = round(random.uniform(50, 95), 1)
                            altura = round(random.uniform(1.50, 1.90), 2)
                            
                            # Dados clínicos
                            tem_doenca = random.random() < 0.7  # 70% tem doença crônica
                            gravidade = random.choice(['Leve', 'Moderada', 'Grave'])
                            tipo_sang = random.choice(tipos_sanguineos)
                            
                            doenca_atual = random.choice(doencas) if tem_doenca else None
                            contagiosa = random.random() < 0.1
                            
                            # Medicamentos
                            num_meds = random.randint(0, 4) if tem_doenca else 0
                            meds_lista = random.sample(medicamentos, min(num_meds, len(medicamentos)))
                            meds_texto = ', '.join(meds_lista)
                            
                            # Necessidades básicas
                            necessidades_opcoes = [
                                'Alimentação regular', 'Acompanhamento médico',
                                'Medicamentos', 'Fraldas geriátricas',
                                'Cadeira de rodas', 'Andador',
                                'Acompanhamento psicológico'
                            ]
                            num_necessidades = random.randint(1, 3)
                            necessidades = ', '.join(random.sample(necessidades_opcoes, num_necessidades))
                            
                            # Auxílio governo
                            auxilio = random.choice([True, False])
                            tipo_auxilio = random.choice([
                                'Bolsa Família', 'BPC', 'Aposentadoria',
                                'Auxílio-Doença', 'Nenhum'
                            ]) if auxilio else 'Nenhum'
                            
                            paciente = Paciente.objects.create(
                                nome=f"{nome_base}",
                                cpf=cpf,
                                idade=idade,
                                peso=peso,
                                altura=altura,
                                cidade='Aracaju',
                                bairro=bairro,
                                endereco=endereco,
                                residencia=residencia,
                                agente=agente,
                                
                                # Novos campos
                                tipo_sanguineo=tipo_sang,
                                doenca_atual=doenca_atual,
                                is_cronica=tem_doenca,
                                is_contagiosa=contagiosa,
                                nivel_gravidade=gravidade if tem_doenca else 'Leve',
                                medicamentos_prescritos=meds_texto,
                                necessidades_basicas=necessidades,
                                recebe_auxilio_governo=auxilio,
                                tipo_auxilio=tipo_auxilio,
                                prontuario_completo=random.choice([True, False]),
                                
                                # Campos originais
                                pessoas_na_casa=qtd_moradores,
                                comorbidade=tem_doenca,
                                comorbidade_tipo=doenca_atual if tem_doenca else '',
                                medicamentos=meds_texto,
                                fuma=random.choice([True, False]),
                                bebe=random.choice([True, False]),
                                atividade_fisica=random.choice([True, False])
                            )
                            pacientes_criados += 1
            
            html += f"<h2>✅ População Concluída!</h2>"
            
            html += "<div class='stats'>"
            html += f"<div class='stat-box'><h3>📍 {residencias_criadas}</h3><p>Residências</p></div>"
            html += f"<div class='stat-box'><h3>👥 {pacientes_criados}</h3><p>Pacientes</p></div>"
            html += f"<div class='stat-box'><h3>🏥 {agentes.count()}</h3><p>Agentes</p></div>"
            html += "</div>"
            
            # Estatísticas por agente
            html += "<h3>📊 Distribuição por Agente:</h3>"
            for agente in agentes:
                qtd_pac = Paciente.objects.filter(agente=agente).count()
                qtd_res = Residencia.objects.filter(agente=agente).count()
                html += f"<p class='info'>• <strong>{agente.usuario.first_name}</strong>: {qtd_pac} pacientes em {qtd_res} residências</p>"
            
            html += "<p class='success' style='margin-top: 30px; font-size: 18px;'>🎉 Dados do mapa atualizados com sucesso!</p>"
            html += "<div style='margin-top: 30px;'>"
            html += "<a href='/mapa/' class='btn' style='background: #27ae60;'>🗺️ Ver Mapa</a> "
            html += "<a href='/login/' class='btn'>🔑 Fazer Login</a>"
            html += "</div>"
            
    except Exception as e:
        html += f"<p style='color: red;'>❌ Erro: {str(e)}</p>"
        import traceback
        html += f"<pre>{traceback.format_exc()}</pre>"
    
    html += "</div></body></html>"
    return HttpResponse(html)
