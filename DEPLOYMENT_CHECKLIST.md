# ✅ Checklist de Deployment - Sistema NVision

## 1️⃣ PREPARAÇÃO (Local)

- [ ] Python 3.7+ instalado (`python --version`)
- [ ] Todos os arquivos do projeto com você
- [ ] Conta no GitHub criada (https://github.com)
- [ ] Git instalado (`git --version`)

## 2️⃣ PREPARAR REPOSITÓRIO GITHUB

### Criar Repo
- [ ] Acesse https://github.com/new
- [ ] Crie repositório (ex: "nvision-system")
- [ ] Copie a URL do repo

### Enviar Código
```bash
# Na pasta do seu projeto:
git init
git add .
git commit -m "Projeto NVision - Deploy Inicial"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/seu-repo.git
git push -u origin main
```

- [ ] Código enviado para GitHub

## 3️⃣ CRIAR ARQUIVO render.yaml

Na raiz do seu projeto, crie arquivo `render.yaml`:

```yaml
services:
- type: web
  name: nvision-system
  runtime: python
  runtimeVersion: 3.11
  buildCommand: pip install -r requirements.txt
  startCommand: python app.py
  envVars:
    - key: FLASK_ENV
      value: production
```

- [ ] Arquivo `render.yaml` criado
- [ ] Commit e push do arquivo

## 4️⃣ ATUALIZAR app.py

Mude a última linha:

### ANTES
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

### DEPOIS
```python
app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

Adicione no topo do arquivo:
```python
import os
```

- [ ] app.py atualizado
- [ ] Teste local (`python app.py` deve funcionar)
- [ ] Commit e push

## 5️⃣ DEPLOY NO RENDER.COM

### Criar Conta
- [ ] Acesse https://render.com
- [ ] Sign up com GitHub
- [ ] Autorize acesso aos repositórios

### Fazer Deploy
- [ ] Clique em "New" → "Web Service"
- [ ] Selecione seu repositório
- [ ] Deixe as configurações automáticas
- [ ] Clique "Create Web Service"
- [ ] Aguarde deployment (3-5 minutos)

### Verificar
- [ ] Veja a URL fornecida (https://seu-app.onrender.com)
- [ ] Acesse a URL no navegador
- [ ] Verifique se o sistema está rodando
- [ ] Cheque "Logs" para erros

## 6️⃣ CONFIGURAR SEGURANÇA

No painel Render:
- [ ] Vá em "Environment"
- [ ] Adicione variável `SECRET_KEY` com valor seguro (ex: gere com `python -c "import os; print(os.urandom(32).hex())"`)
- [ ] Salve

## 7️⃣ USAR A APLICAÇÃO

- [ ] Acesse: `https://seu-app.onrender.com`
- [ ] Login padrão: `admin` / `admin123`
- [ ] Teste criar um chamado
- [ ] Teste gerar relatório

## 8️⃣ DOMÍNIO CUSTOMIZADO (Opcional)

Se quiser um domínio melhor:
- [ ] Compre domínio (Google Domains, Namecheap, etc)
- [ ] No Render, vá em "Settings" → "Custom Domain"
- [ ] Adicione seu domínio
- [ ] Configure DNS conforme instruído

## ⚠️ PROBLEMAS COMUNS

### App dorme após 15 minutos (Render free)
✅ Normal no plano gratuito
✅ Primeira requisição demora ~30s para acordar
✅ Mude para plano pago se precisar 24/7

### Erro "App crashed"
- Verifique logs no Render
- Confirme que `app.py` tem porta `0.0.0.0` e variável `PORT`
- Teste localmente: `python app.py`

### Banco de dados vazio
- Pode ser reset ao fazer deploy
- Dados em SQLite não persistem bem em servidores
- **Solução**: Mude para PostgreSQL (Render inclui grátis)

### Erro de import de módulos
- Verifique `requirements.txt`
- Execute localmente: `pip install -r requirements.txt`
- Commit e push novamente

## 📊 PRÓXIMOS PASSOS

### Melhorias Recomendadas
- [ ] Migrar de SQLite para PostgreSQL
- [ ] Adicionar backup automático
- [ ] Configurar alertas de erros
- [ ] Adicionar SSL/TLS (Render faz automático)

### Monitoramento
- [ ] Verificar logs regularmente
- [ ] Monitorar CPU/memória
- [ ] Testar performance com usuários reais

---

**Data de Deploy:** _______________  
**URL de Produção:** https://___________________.onrender.com  
**Status:** ✅ Ativo / ⏸️ Inativo / ❌ Problema  

---

*Documento de acompanhamento para seu deployment*
