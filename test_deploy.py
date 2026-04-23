#!/usr/bin/env python3
"""
Script para testar se seu sistema está pronto para deployment
Antes de fazer push para Render, execute este script
"""

import os
import sys
import importlib.util

def check(description, condition):
    """Função auxiliar para verificações"""
    status = "✅ OK" if condition else "❌ FALHA"
    print(f"  {status} - {description}")
    return condition

def load_module(name, path):
    """Carrega um módulo Python dinamicamente"""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None

print("\n" + "="*60)
print("🔍 VERIFICAÇÃO PRÉ-DEPLOYMENT")
print("="*60 + "\n")

all_good = True

# 1. Verificar arquivos necessários
print("1️⃣  Arquivos Necessários:")
files_to_check = [
    'app.py',
    'database.py',
    'reports.py',
    'requirements.txt',
    'templates'
]
for file in files_to_check:
    result = os.path.exists(file)
    if not check(f"Arquivo/Pasta '{file}' existe", result):
        all_good = False

# 2. Verificar Python
print("\n2️⃣  Versão do Python:")
version = sys.version_info
valid_version = version.major >= 3 and version.minor >= 7
if not check(f"Python {version.major}.{version.minor} (necessário 3.7+)", valid_version):
    all_good = False

# 3. Verificar dependências
print("\n3️⃣  Dependências Instaladas:")
required_packages = [
    'flask',
    'flask_sqlalchemy',
    'dateutil',
    'reportlab',
    'matplotlib',
    'PIL'
]

for package in required_packages:
    try:
        __import__(package)
        check(f"Módulo '{package}' disponível", True)
    except ImportError:
        check(f"Módulo '{package}' disponível", False)
        all_good = False

# 4. Tentar carregar app.py
print("\n4️⃣  Integridade da Aplicação:")
try:
    app_module = load_module('app', 'app.py')
    if app_module and hasattr(app_module, 'app'):
        check("app.py pode ser carregado", True)
        check("Aplicação Flask existe", True)
    else:
        check("app.py pode ser carregado", False)
        all_good = False
except Exception as e:
    check(f"app.py pode ser carregado", False)
    print(f"    Erro: {e}")
    all_good = False

# 5. Verificar database.py
print("\n5️⃣  Banco de Dados:")
try:
    db_module = load_module('database', 'database.py')
    if db_module:
        check("database.py pode ser carregado", True)
    else:
        check("database.py pode ser carregado", False)
        all_good = False
except Exception as e:
    check("database.py pode ser carregado", False)
    print(f"    Erro: {e}")
    all_good = False

# 6. Verificar requirements.txt
print("\n6️⃣  requirements.txt:")
try:
    with open('requirements.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
        check(f"requirements.txt tem {len(lines)} dependências", len(lines) > 0)
except:
    check("requirements.txt pode ser lido", False)
    all_good = False

# 7. Verificar configurações de deployment
print("\n7️⃣  Configuração para Deployment:")
try:
    with open('app.py', 'r') as f:
        content = f.read()
        has_port_env = 'os.environ.get' in content and 'PORT' in content
        has_host_0000 = '0.0.0.0' in content

        check("app.py usa PORT da variável de ambiente", has_port_env)
        check("app.py usa host='0.0.0.0' (não 127.0.0.1)", has_host_0000)

        if not (has_port_env and has_host_0000):
            print("    ⚠️  AVISO: Configure a última linha do app.py para:")
            print("    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))")
            all_good = False
except:
    check("app.py pode ser verificado", False)
    all_good = False

# 8. Verificar render.yaml
print("\n8️⃣  Arquivo render.yaml:")
if os.path.exists('render.yaml'):
    check("render.yaml existe", True)
    with open('render.yaml', 'r') as f:
        content = f.read()
        check("render.yaml tem configuração web", 'type: web' in content)
        check("render.yaml tem startCommand", 'startCommand:' in content)
else:
    check("render.yaml existe", False)
    print("    ⚠️  Crie render.yaml na raiz do projeto com:")
    print("""
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
    """)
    all_good = False

# Resultado Final
print("\n" + "="*60)
if all_good:
    print("✅ TUDO OK! Seu sistema está pronto para deployment")
    print("="*60)
    print("\nPróximos passos:")
    print("1. git add .")
    print("2. git commit -m 'Pronto para deployment'")
    print("3. git push origin main")
    print("4. Acesse https://render.com e faça o deployment")
    sys.exit(0)
else:
    print("❌ Alguns problemas foram encontrados")
    print("="*60)
    print("\nCorreja os itens acima e tente novamente")
    sys.exit(1)
