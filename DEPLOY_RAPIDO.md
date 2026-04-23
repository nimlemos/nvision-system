# 🚀 DEPLOY RÁPIDO - NVision em 5 Minutos

## Pré-requisitos
- ✅ Conta no GitHub (grátis em https://github.com)
- ✅ Conta no Render.com (grátis em https://render.com)
- ✅ Git instalado (https://git-scm.com/download)

---

## PASSO 1: Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Preencha:
   - **Repository name**: `nvision-system` (ou outro nome)
   - Deixe público (Public)
   - Clique **"Create repository"**

3. **Copie a URL** que aparece (exemplo: `https://github.com/seu-usuario/nvision-system.git`)

---

## PASSO 2: Enviar Código para GitHub

Abra o terminal/PowerShell na pasta do seu projeto e execute:

```bash
git init
git add .
git commit -m "Projeto NVision - Pronto para Deploy"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

**Substitua:**
- `SEU_USUARIO` = seu nome de usuário do GitHub
- `SEU_REPO` = nome do repositório que criou (ex: `nvision-system`)

✅ Pronto! Seu código está no GitHub

---

## PASSO 3: Deploy no Render.com

1. Acesse https://render.com
2. Clique em **"Sign Up"** → escolha **"Continue with GitHub"**
3. Autorize o Render a acessar seus repositórios
4. No dashboard do Render, clique em **"New"** → **"Web Service"**
5. Selecione o repositório `nvision-system`
6. Configure:
   - **Name**: `nvision-system`
   - **Runtime**: Python (automático)
   - Deixe o resto como está
7. Clique em **"Create Web Service"**

⏳ Aguarde 3-5 minutos enquanto o Render:
   - Baixa o código
   - Instala as dependências
   - Inicia o servidor

---

## PASSO 4: Acessar Seu Aplicativo

Quando terminar, Render mostrará uma URL como:
```
https://nvision-system.onrender.com
```

Clique nela ou copie para acessar seu sistema!

### Login Padrão
- **Usuário**: `admin`
- **Senha**: `admin123`

---

## 🎯 Pronto!

Seu sistema está rodando na **nuvem gratuita** e acessível de qualquer lugar! 🌍

### Para atualizações futuras:
1. Faça mudanças no código localmente
2. `git add . && git commit -m "descrição" && git push origin main`
3. Render redeploy automaticamente

---

## ⚠️ Importante Saber

### O app dorme após 15 minutos
- Isso é **normal no plano gratuito** do Render
- Primeira requisição demora ~30 segundos
- Para usar 24/7 sem dormir, considere upgrade (pago)

### Dados persistem?
- ✅ Banco de dados SQLite persiste entre deploys
- ⚠️ Pode ter problemas com múltiplos usuários simultâneos
- 💡 Para produção, considere migrar para PostgreSQL (grátis no Render)

---

## 🆘 Troubleshooting

### Erro no deployment?
→ Verifique os logs no Render (aba "Logs")

### Aplicação não carrega?
→ Aguarde 30 segundos (app está acordando)

### Dados desapareceram?
→ SQLite pode ser resetado durante deploys
→ Solução: Use PostgreSQL

### Quer um domínio customizado?
→ Compre em Google Domains ou Namecheap
→ Configure em Render → Settings → Custom Domain

---

## 📞 Próximos Passos

1. **Backup**: Faça backup da pasta localmente
2. **Segurança**: Mude a senha do admin após primeiro acesso
3. **Domínio**: Configure domínio personalizado (opcional)
4. **Monitoramento**: Verifique logs regularmente

---

**Dúvidas?** Consulte o `Guia_Deployment_Sistema_Python.docx` para mais detalhes!
