# 🏥 Saúde Conectada

Sistema de gestão de saúde com Django para Médicos, Agentes de Saúde e Pacientes.

## 🚀 Deploy Rápido no Railway

### Passo 1: Preparar o Repositório Git

```bash
git init
git add .
git commit -m "Initial commit - Saúde Conectada"
```

### Passo 2: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com/) e crie um novo repositório
2. **Não** inicialize com README, .gitignore ou licença
3. Copie a URL do repositório

```bash
git remote add origin https://github.com/seu-usuario/saude-conectada.git
git branch -M main
git push -u origin main
```

### Passo 3: Deploy no Railway

1. Acesse [Railway.app](https://railway.app/)
2. Faça login com GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório **saude-conectada**
6. Railway detectará automaticamente o Django e começará o deploy

### Passo 4: Configurar Variáveis de Ambiente

No painel do Railway, clique em **Variables** e adicione:

```
SECRET_KEY=django-seu-secret-key-super-seguro-123456789
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

**Para gerar um SECRET_KEY seguro:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Passo 5: Adicionar PostgreSQL (Recomendado)

1. No projeto Railway, clique em **"New"**
2. Selecione **"Database"** → **"Add PostgreSQL"**
3. Railway conectará automaticamente ao Django
4. A variável `DATABASE_URL` será configurada automaticamente

### Passo 6: Criar Dados de Teste

Após o deploy, use o Railway CLI:

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Fazer login
railway login

# Conectar ao projeto
railway link

# Criar dados de teste
railway run python create_test_data.py
```

**Ou use o console web do Railway:**
1. Vá em "Settings" → "Deploy Logs"
2. Execute: `python create_test_data.py`

### Passo 7: Acessar o App

Sua URL será algo como: `https://seu-app.railway.app`

## 🔑 Credenciais de Teste

- **Admin:** admin / 123
- **Agente:** AG001 / 123
- **Médico:** CRM12345 / 123
- **Paciente:** 111.222.333-44 / 123

## 📦 Arquivos Criados para Deploy

- ✅ `Procfile` - Comando para iniciar o Gunicorn
- ✅ `runtime.txt` - Versão do Python
- ✅ `railway.json` - Configuração Railway
- ✅ `nixpacks.toml` - Build configuration
- ✅ `requirements.txt` - Dependências atualizadas
- ✅ `.gitignore` - Arquivos a ignorar
- ✅ `create_test_data.py` - Script para dados de teste

## 🛠️ Desenvolvimento Local

```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar dados de teste
python create_test_data.py

# Iniciar servidor
python manage.py runserver
```

## 📝 Checklist Pré-Deploy

- [x] Requirements.txt atualizado
- [x] Gunicorn instalado
- [x] WhiteNoise para arquivos estáticos
- [x] python-decouple para variáveis de ambiente
- [x] dj-database-url para PostgreSQL
- [x] Settings.py configurado para produção
- [x] Procfile criado
- [x] .gitignore configurado
- [x] Script de dados de teste

## ✅ App Pronto para Deploy!

O app está 100% pronto para deploy no Railway. Siga os passos acima e em 5 minutos estará no ar!
