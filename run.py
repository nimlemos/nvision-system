#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import webbrowser
import time

def check_and_install_requirements():
    """Verifica e instala as dependências necessárias"""
    print("\n" + "="*60)
    print("  🚀 Nvision Informatica - Sistema de Atendimento")
    print("="*60 + "\n")

    print("📦 Verificando dependências...\n")

    try:
        requirements = [
            'Flask==2.3.3',
            'Flask-SQLAlchemy==3.0.5',
            'python-dateutil==2.8.2',
            'reportlab==4.0.7',
            'matplotlib==3.7.2',
            'Pillow==10.0.0',
        ]

        # Verificar se pip está disponível
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

        # Instalar requirements
        print("📥 Instalando pacotes necessários...\n")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

        print("\n✅ Dependências instaladas com sucesso!\n")
        return True

    except Exception as e:
        print(f"\n❌ Erro ao instalar dependências: {e}")
        print("\nTente executar manualmente:")
        print(f"  {sys.executable} -m pip install -r requirements.txt\n")
        return False


def start_server():
    """Inicia o servidor Flask"""
    print("\n" + "="*60)
    print("  ✨ Iniciando servidor...")
    print("="*60 + "\n")

    try:
        # Adicionar o diretório atual ao path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Importar e executar a app
        from app import app

        print("🌐 Servidor rodando em: http://localhost:5000")
        print("📱 Abra seu navegador e acesse o endereço acima")
        print("\n⏹️  Pressione Ctrl+C para parar o servidor\n")
        print("="*60 + "\n")

        # Abrir navegador automaticamente após 2 segundos
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')

        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Rodar o servidor
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        print("\nTente executar manualmente:")
        print("  python app.py\n")
        sys.exit(1)


if __name__ == '__main__':
    # Verificar e instalar dependências
    if check_and_install_requirements():
        # Iniciar servidor
        start_server()
    else:
        sys.exit(1)
