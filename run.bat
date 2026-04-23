@echo off
REM Script para executar o Sistema de Atendimento Nvision no Windows

chcp 65001 > nul
cls

echo.
echo ============================================================
echo   🚀 Nvision Informatica - Sistema de Atendimento
echo ============================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo Por favor, instale Python 3.7+ em:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.
echo 📦 Instalando dependências...
echo.

REM Instalar dependências
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ Erro ao instalar dependências
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dependências instaladas com sucesso!
echo.
echo ============================================================
echo   ✨ Iniciando servidor...
echo ============================================================
echo.
echo 🌐 Servidor rodando em: http://localhost:5000
echo 📱 Seu navegador será aberto automaticamente
echo.
echo ⏹️  Pressione Ctrl+C para parar o servidor
echo.
echo ============================================================
echo.

REM Iniciar o servidor
python run.py

pause
