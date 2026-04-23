@echo off
REM ============================================================
REM  🚀 NVISION INFORMATICA - Acesso Rápido
REM  Script para iniciar o sistema em um clique
REM ============================================================

chcp 65001 > nul
cls

echo.
echo ════════════════════════════════════════════════════════════
echo.
echo   🚀 NVISION INFORMATICA
echo   Sistema de Gerenciamento de Atendimento
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo.
    echo Instale Python 3.7+ em: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.
echo 📦 Verificando dependências...
echo.

REM Instalar dependências silenciosamente
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -q -r requirements.txt 2>nul

echo ✅ Sistema pronto!
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo   ✨ Iniciando servidor...
echo.
echo   🌐 Acesse em: http://localhost:5000
echo   📱 O navegador será aberto automaticamente
echo.
echo   ⏹️  Pressione Ctrl+C para parar
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Iniciar servidor
python EXECUTE.py

pause
