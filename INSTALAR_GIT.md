# 🔧 Como Instalar Git

Git é necessário para fazer upload do seu código para GitHub.

## Windows

### Opção 1: Instalador Simples (Recomendado)
1. Acesse: https://git-scm.com/download/win
2. Clique no arquivo `.exe` (vai baixar automaticamente)
3. Abra o arquivo baixado
4. Clique "Next" até o final, tudo padrão está bom
5. Pronto!

### Opção 2: Chocolatey (se tiver)
```bash
choco install git
```

### Verificar Instalação
Abra PowerShell ou CMD e digite:
```bash
git --version
```
Deve mostrar algo como: `git version 2.40.0`

---

## macOS

### Opção 1: Usando Homebrew (se tiver)
```bash
brew install git
```

### Opção 2: Instalador Oficial
1. Acesse: https://git-scm.com/download/mac
2. Clique no instalador `.dmg`
3. Siga as instruções

### Verificar Instalação
```bash
git --version
```

---

## Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install git
```

Verificar:
```bash
git --version
```

---

## Depois de Instalar: Configuração Inicial

Na primeira vez, configure seu nome e email:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

Exemplo:
```bash
git config --global user.name "Nilton Lemos"
git config --global user.email "informaticanvision@gmail.com"
```

---

## ✅ Está Tudo Pronto?

1. Abra terminal/PowerShell
2. Digite: `git --version`
3. Se mostrar versão, tudo certo!

---

## 🆘 Problema?

Se receber erro "git não é reconhecido":
1. Reinicie o PC após instalar
2. Use o "Git Bash" (instalado junto com Git no Windows)
3. Se ainda não funcionar, reinstale Git

---

**Próximo passo:** Leia `DEPLOY_RAPIDO.md`
