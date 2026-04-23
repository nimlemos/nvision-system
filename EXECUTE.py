#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚀 NVISION INFORMATICA - Acesso Rápido ao Sistema
Script único para instalar, executar e abrir no navegador
"""

import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

class Cores:
    """Cores para terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    """Exibe logo do sistema"""
    print(f"\n{Cores.BOLD}{Cores.CYAN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║          🚀 NVISION INFORMATICA                            ║")
    print("║          Sistema de Gerenciamento de Atendimento           ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Cores.END}\n")

def verificar_python():
    """Verifica se Python está instalado corretamente"""
    print(f"{Cores.BLUE}📍 Verificando Python...{Cores.END}")

    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print(f"{Cores.RED}❌ Python 3.7+ necessário (você tem {version.major}.{version.minor}){Cores.END}\n")
            return False

        print(f"{Cores.GREEN}✅ Python {version.major}.{version.minor} detectado{Cores.END}\n")
        return True
    except Exception as e:
        print(f"{Cores.RED}❌ Erro: {e}{Cores.END}\n")
        return False

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print(f"{Cores.BLUE}📦 Instalando dependências...{Cores.END}")
    print(f"{Cores.YELLOW}   Isso pode levar alguns minutos na primeira execução{Cores.END}\n")

    try:
        # Atualizar pip
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Instalar requirements
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print(f"{Cores.GREEN}✅ Dependências instaladas com sucesso!{Cores.END}\n")
        return True

    except subprocess.CalledProcessError as e:
        print(f"{Cores.RED}❌ Erro ao instalar dependências{Cores.END}")
        print(f"{Cores.RED}   {e}{Cores.END}\n")
        return False
    except Exception as e:
        print(f"{Cores.RED}❌ Erro inesperado: {e}{Cores.END}\n")
        return False

def verificar_dependencias():
    """Verifica se as dependências já estão instaladas"""
    print(f"{Cores.BLUE}🔍 Verificando pacotes...{Cores.END}")

    try:
        import flask
        import flask_sqlalchemy
        import reportlab
        import matplotlib
        print(f"{Cores.GREEN}✅ Todos os pacotes já estão instalados!{Cores.END}\n")
        return True
    except ImportError:
        print(f"{Cores.YELLOW}⚠️  Alguns pacotes não estão instalados{Cores.END}\n")
        return False

def abrir_navegador():
    """Abre o navegador após 3 segundos"""
    def _abrir():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:5000')
            print(f"\n{Cores.GREEN}✅ Navegador aberto automaticamente!{Cores.END}")
            print(f"{Cores.CYAN}   http://localhost:5000{Cores.END}\n")
        except:
            pass

    thread = threading.Thread(target=_abrir, daemon=True)
    thread.start()

def iniciar_servidor():
    """Inicia o servidor Flask"""
    print(f"{Cores.GREEN}{'='*60}{Cores.END}")
    print(f"{Cores.BOLD}{Cores.GREEN}✨ SERVIDOR INICIADO!{Cores.END}")
    print(f"{Cores.GREEN}{'='*60}{Cores.END}\n")

    print(f"{Cores.CYAN}🌐 Acesse em: {Cores.BOLD}http://localhost:5000{Cores.END}\n")
    print(f"{Cores.YELLOW}📍 Abrindo navegador automaticamente...{Cores.END}\n")

    # Abrir navegador
    abrir_navegador()

    print(f"{Cores.YELLOW}{'='*60}{Cores.END}")
    print(f"{Cores.YELLOW}⏹️  Pressione Ctrl+C para parar o servidor{Cores.END}")
    print(f"{Cores.YELLOW}{'='*60}{Cores.END}\n")

    try:
        # Importar e executar a app
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app

        # Executar servidor
        app.run(
            debug=True,
            host='127.0.0.1',
            port=5000,
            use_reloader=False,
            use_debugger=False
        )

    except KeyboardInterrupt:
        print(f"\n{Cores.YELLOW}⏹️  Servidor parado pelo usuário{Cores.END}\n")
    except Exception as e:
        print(f"{Cores.RED}❌ Erro ao iniciar servidor: {e}{Cores.END}\n")
        sys.exit(1)

def main():
    """Função principal"""
    limpar_tela()
    print_logo()

    # 1. Verificar Python
    if not verificar_python():
        print(f"{Cores.RED}❌ Python não está configurado corretamente{Cores.END}\n")
        sys.exit(1)

    # 2. Verificar e instalar dependências
    if not verificar_dependencias():
        if not instalar_dependencias():
            print(f"{Cores.RED}❌ Falha ao instalar dependências{Cores.END}\n")
            sys.exit(1)

    # 3. Iniciar servidor
    try:
        iniciar_servidor()
    except KeyboardInterrupt:
        print(f"\n{Cores.YELLOW}Encerrando...{Cores.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{Cores.RED}❌ Erro fatal: {e}{Cores.END}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
