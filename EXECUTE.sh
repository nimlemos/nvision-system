#!/bin/bash

# 🚀 NVISION INFORMATICA - Acesso Rápido
# Script para iniciar o sistema em um clique

clear

echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "   🚀 NVISION INFORMATICA"
echo "   Sistema de Gerenciamento de Atendimento"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo ""
    echo "Instale Python 3.7+ em: https://www.python.org/downloads/"
    echo ""
    read -p "Pressione Enter para sair..."
    exit 1
fi

echo "✅ Python detectado"
echo ""
echo "📦 Verificando dependências..."
echo ""

# Instalar dependências
python3 -m pip install --upgrade pip > /dev/null 2>&1
python3 -m pip install -r requirements.txt > /dev/null 2>&1

echo "✅ Sistema pronto!"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "   ✨ Iniciando servidor..."
echo ""
echo "   🌐 Acesse em: http://localhost:5000"
echo "   📱 O navegador será aberto automaticamente"
echo ""
echo "   ⏹️  Pressione Ctrl+C para parar"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Iniciar servidor
python3 EXECUTE.py
