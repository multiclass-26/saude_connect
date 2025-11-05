# ✅ CHECKLIST PRÉ-DEPLOY

## Arquivos de Configuração

- [x] `Procfile` - Comando Gunicorn
- [x] `runtime.txt` - Python 3.11
- [x] `railway.json` - Configuração Railway
- [x] `nixpacks.toml` - Build settings
- [x] `.gitignore` - Ignorar arquivos desnecessários
- [x] `.env.example` - Exemplo de variáveis

## Dependências

- [x] `Django>=5.0` - Framework principal
- [x] `gunicorn>=21.0` - Servidor WSGI
- [x] `whitenoise>=6.0` - Arquivos estáticos
- [x] `python-decouple>=3.8` - Variáveis de ambiente
- [x] `dj-database-url>=2.0` - Database URL parser
- [x] `psycopg2-binary>=2.9` - PostgreSQL adapter
- [x] `Pillow>=10.0` - Imagens
- [x] `djangorestframework>=3.14` - REST API
- [x] `django-cors-headers>=4.0` - CORS

## Settings.py

- [x] SECRET_KEY via environment variable
- [x] DEBUG via environment variable
- [x] ALLOWED_HOSTS configurável
- [x] WhiteNoise middleware
- [x] Database URL dinâmica
- [x] Static files com WhiteNoise
- [x] Security settings para produção

## Arquivos Estáticos

- [x] `STATIC_ROOT` configurado
- [x] `STATIC_URL` definido
- [x] `STATICFILES_DIRS` com pasta static
- [x] WhiteNoise storage configurado

## Banco de Dados

- [x] SQLite para desenvolvimento
- [x] PostgreSQL pronto para produção
- [x] Migrações criadas
- [x] Models testados

## Scripts

- [x] `create_test_data.py` - Criar usuários de teste
- [x] Script funciona em produção

## Documentação

- [x] `README.md` completo
- [x] `DEPLOY_RAILWAY.md` passo a passo
- [x] Credenciais de teste documentadas

## Testes Locais

Execute antes de fazer deploy:

```bash
# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar novas dependências
pip install -r requirements.txt

# Testar collectstatic
python manage.py collectstatic --noinput

# Rodar servidor
python manage.py runserver
```

## Comandos de Deploy

```bash
# 1. Git
git init
git add .
git commit -m "Deploy inicial"

# 2. GitHub
git remote add origin https://github.com/usuario/repo.git
git push -u origin main

# 3. Railway
# Seguir DEPLOY_RAILWAY.md
```

## Variáveis de Ambiente Necessárias

```
SECRET_KEY=seu-secret-key-aqui
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

## Opcional mas Recomendado

- [ ] Adicionar PostgreSQL no Railway
- [ ] Configurar domínio customizado
- [ ] Adicionar monitoramento
- [ ] Configurar backups

## ✅ TUDO PRONTO!

Seu app está 100% configurado para deploy no Railway.
Siga o guia em `DEPLOY_RAILWAY.md`
