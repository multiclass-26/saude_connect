# 🏥 Saúde Conectada

Sistema de gestão de saúde com Django para Médicos, Agentes de Saúde e Pacientes.

## 🚀 Deploy Automático no Railway

### Passo 1: Criar Repositório no GitHub

```bash
git init
git add .
git commit -m "Initial commit - Saúde Conectada"
```

1. Acesse [GitHub](https://github.com/) e crie um novo repositório
2. **Não** inicialize com README, .gitignore ou licença

```bash
git remote add origin https://github.com/seu-usuario/saude-conectada.git
git branch -M main
git push -u origin main
```

### Passo 2: Deploy no Railway

1. Acesse [Railway.app](https://railway.app/)
2. Faça login com GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório **saude-conectada**

✅ **O Railway executará automaticamente:**
- Instalação de dependências
- Migrações do banco de dados
- **Criação automática dos usuários de teste**
- Inicialização do servidor

### Passo 3: Configurar Variáveis de Ambiente

No painel do Railway, clique em **Variables** e adicione:

```
SECRET_KEY=django-seu-secret-key-super-seguro-123456789
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

**Para gerar um SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Passo 4 (Opcional): Adicionar PostgreSQL

1. No projeto Railway, clique em **"New"** → **"Database"** → **"PostgreSQL"**
2. A conexão é configurada automaticamente via `DATABASE_URL`

## 🔑 Credenciais de Teste (Criadas Automaticamente)

| Tipo | Usuário | Senha |
|------|---------|-------|
| **Admin** | `admin` | `123` |
| **Médico** | `medico` | `123` |
| **Agente** | `agente` | `123` |
| **Paciente** | `paciente` | `123` |

## 🛠️ Desenvolvimento Local

```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar migrações e criar usuários automaticamente
python manage.py migrate
python manage.py create_users

# Iniciar servidor
python manage.py runserver
```

Acesse: `http://localhost:8000`

## 📦 Estrutura do Projeto

```
app_saude_connect/
├── accounts/           # Autenticação e usuários
│   ├── management/
│   │   └── commands/
│   │       └── create_users.py  # Criação automática de usuários
├── patients/          # Gestão de pacientes
├── reminders/         # Lembretes e notificações
├── config/            # Configurações do Django
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── templates/         # Templates HTML
├── Procfile           # Comando Railway (com criação automática de usuários)
├── requirements.txt   # Dependências Python
└── runtime.txt        # Versão do Python
```

## ✨ Recursos

- ✅ Login simplificado (usuário + senha)
- ✅ Dashboards personalizados por tipo de usuário
- ✅ Vídeos educativos de exercícios e saúde
- ✅ Sistema de notificações
- ✅ Interface acessível com ícones
- ✅ Deploy automático no Railway
- ✅ Criação automática de usuários de teste

## 🔧 Tecnologias

- Django 5.2.7
- Python 3.12
- SQLite (local) / PostgreSQL (produção)
- WhiteNoise para arquivos estáticos
- Gunicorn como servidor WSGI

## 📝 Procfile (Configuração Railway)

```
web: python manage.py migrate && python manage.py create_users && gunicorn config.wsgi --log-file -
```

Este comando garante que a cada deploy:
1. As migrações são executadas
2. Os usuários de teste são criados automaticamente
3. O servidor Gunicorn é iniciado

## ✅ Pronto para Produção!

O aplicativo está 100% configurado para deploy no Railway com criação automática de usuários.
