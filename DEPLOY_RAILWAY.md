# 🚀 GUIA RÁPIDO DE DEPLOY NO RAILWAY

## Tempo Estimado: 5 minutos

### 1️⃣ PREPARAR GIT (2 min)

```bash
# Abrir terminal no diretório do projeto
cd C:\Users\andre\Documents\proj_pessoal\app_saude_django

# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy Saúde Conectada"
```

### 2️⃣ GITHUB (1 min)

1. Acesse: https://github.com/new
2. Nome: `saude-conectada`
3. NÃO marque nenhuma opção
4. Clique em "Create repository"
5. Copie os comandos mostrados:

```bash
git remote add origin https://github.com/SEU-USUARIO/saude-conectada.git
git branch -M main
git push -u origin main
```

### 3️⃣ RAILWAY (2 min)

1. Acesse: https://railway.app/
2. Login com GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecione `saude-conectada`
5. Aguarde o deploy (1-2 min)

### 4️⃣ CONFIGURAR VARIÁVEIS

No Railway, clique em "Variables" e adicione:

```
SECRET_KEY=cole-aqui-um-secret-key-seguro
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

**Gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5️⃣ ADICIONAR POSTGRESQL (OPCIONAL)

1. No projeto Railway: "New" → "Database" → "PostgreSQL"
2. Aguarde conexão automática
3. Railway adicionará `DATABASE_URL` automaticamente

### 6️⃣ CRIAR DADOS DE TESTE

Opção A - Railway CLI:
```bash
npm i -g @railway/cli
railway login
railway link
railway run python create_test_data.py
```

Opção B - Console Web:
1. Railway → "Settings" → "Deploy Logs"
2. Execute: `python create_test_data.py`

### ✅ PRONTO!

Seu app estará em: `https://seu-projeto.railway.app`

## 🔑 Credenciais de Teste

- Admin: admin / 123
- Agente: AG001 / 123
- Médico: CRM12345 / 123
- Paciente: 111.222.333-44 / 123

## ⚠️ PROBLEMAS COMUNS

**Build falhou?**
- Verifique se todos os arquivos foram commitados
- Confira o `requirements.txt`

**Página não abre?**
- Aguarde 2-3 minutos após o deploy
- Verifique as variáveis de ambiente

**Erro de static files?**
- Railway executa automaticamente `collectstatic`
- Verifique os logs em "Deployments"

## 📞 SUPORTE

- Logs do Railway: aba "Deployments"
- Docs: https://docs.railway.app/
