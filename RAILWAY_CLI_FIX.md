# 🚂 Corrigir Usuários no Railway

## ✅ SOLUÇÃO RÁPIDA (Recomendado)

### 1️⃣ Acesse a URL do Setup

Abra no navegador:
```
https://saudeconnect.com.br/setup/
```

Esta página vai **automaticamente**:
- ✓ Criar/resetar todos os 6 usuários
- ✓ Configurar as senhas corretas
- ✓ Criar perfis de médicos e agentes
- ✓ Mostrar todas as credenciais

### 2️⃣ Credenciais após Setup

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

### 3️⃣ Teste o Login

Após executar o setup, acesse:
```
https://saudeconnect.com.br/login/
```

Faça login com qualquer uma das credenciais acima.

---

Se preferir usar o Railway CLI:

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
- Selecione seu projeto "saude_connect"

### 4️⃣ Executar Comando Django

Execute o comando personalizado para resetar usuários:

```bash
railway run python manage.py resetar_usuarios
```

**Nota:** O comando `railway run` executa **localmente** mas com as variáveis do Railway. Para executar no servidor, use a página `/setup/` conforme método recomendado acima.

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
