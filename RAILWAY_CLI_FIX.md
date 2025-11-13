# 🚂 Corrigir Usuários no Railway via CLI

## 📋 Passo a Passo

### 1️⃣ Instalar Railway CLI (se ainda não tiver)

**Windows (PowerShell):**
```powershell
iwr https://railway.app/install.ps1 | iex
```

**Ou via npm:**
```bash
npm install -g @railway/cli
```

### 2️⃣ Fazer Login no Railway

```bash
railway login
```
- Vai abrir o navegador
- Faça login na sua conta Railway

### 3️⃣ Vincular ao Projeto

Na pasta do projeto:
```bash
cd C:\Users\andre\Documents\Unit\app_saude_connect
railway link
```
- Selecione seu projeto "saude_connect" (ou o nome que você deu)

### 4️⃣ Resetar Usuários no Railway

Execute o script para criar/resetar as senhas:

```bash
railway run python resetar_usuarios_railway.py
```

**OU** se não funcionar, tente:

```bash
railway shell
python resetar_usuarios_railway.py
exit
```

### 5️⃣ Credenciais após Reset

```
MÉDICOS:
  • admin / admin123 (Superusuário)
  • medico / medico123

AGENTES DE SAÚDE:
  • agente / agente123 (Paulo)
  • andre_agente / agente123 (André)
  • fernanda_agente / agente123 (Fernanda)

PACIENTE:
  • paciente / paciente123
```

---

## 🔧 Comandos Úteis do Railway CLI

### Ver logs do projeto:
```bash
railway logs
```

### Abrir shell interativo:
```bash
railway shell
```

### Executar migrations:
```bash
railway run python manage.py migrate
```

### Criar superusuário diretamente:
```bash
railway run python manage.py createsuperuser
```

### Popular dados no Railway:
```bash
railway run python configurar_areas_agentes.py
railway run python popular_mapa_expandido.py
```

### Ver variáveis de ambiente:
```bash
railway variables
```

---

## 🚨 Troubleshooting

### Erro: "railway: command not found"
Reinicie o terminal após instalar o CLI

### Erro: "No project found"
Execute `railway link` para vincular ao projeto

### Erro ao executar script:
1. Verifique se o script foi commitado e está no Railway:
```bash
git add resetar_usuarios_railway.py
git commit -m "Add reset users script"
git push
```

2. Aguarde o deploy completar

3. Execute novamente:
```bash
railway run python resetar_usuarios_railway.py
```

### Alternativa: Criar usuário via Shell

```bash
railway shell
```

Dentro do shell:
```python
python manage.py shell

from accounts.models import Usuario

# Resetar senha do admin
admin = Usuario.objects.get(username='admin')
admin.set_password('admin123')
admin.save()

# Resetar senha do agente
agente = Usuario.objects.get(username='agente')
agente.set_password('agente123')
agente.save()

exit()
```

---

## 📊 Verificar se funcionou

Após executar o script, acesse sua URL do Railway e tente fazer login com:
- **admin** / **admin123**

Se funcionar, está tudo certo! ✅

---

## 🎯 Checklist

- [ ] Railway CLI instalado
- [ ] Login feito (`railway login`)
- [ ] Projeto vinculado (`railway link`)
- [ ] Script executado (`railway run python resetar_usuarios_railway.py`)
- [ ] Login testado no site
- [ ] ✅ Funcionando!
