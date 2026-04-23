#!/bin/bash

# Script para executar o Sistema de Atendimento Nvision no Mac/Linux

echo ""
echo "============================================================"
echo "  🚀 Nvision Informatica - Sistema de Atendimento"
echo "============================================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo ""
    echo "Por favor, instale Python 3.7+ em:"
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "✅ Python detectado"
echo ""
echo "📦 Instalando dependências..."
echo ""

# Instalar dependências
python3 -m pip install --upgrade pip > /dev/null 2>&1
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao instalar dependências"
    echo ""
    exit 1
fi

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "============================================================"
echo "   ✨ Iniciando servidor..."
echo "============================================================"
echo ""
echo "🌐 Servidor rodando em: http://localhost:5000"
echo "📱 Seu navegador será aberto automaticamente"
echo ""
echo "⏹️  Pressione Ctrl+C para parar o servidor"
echo ""
echo "============================================================"
echo ""

# Iniciar o servidor
python3 run.py
