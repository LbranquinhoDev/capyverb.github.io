import os
import sys

print("🔄 RECUPERAÇÃO DE EMERGÊNCIA")
print(f"Diretório atual: {os.getcwd()}")
print(f"Arquivos: {os.listdir('.')}")

# Verificar se setup_postgres.py existe
if 'setup_postgres.py' in os.listdir('.'):
    print("✅ setup_postgres.py encontrado")
    # Executar
    exec(open('setup_postgres.py').read())
else:
    print("❌ setup_postgres.py NÃO encontrado")
    print("📋 Criando script básico...")
    
    # Criar script básico
    basic_script = '''
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "capyverb.settings")
django.setup()

print("✅ Django configurado")

# Migrações
from django.core.management import execute_from_command_line
execute_from_command_line(["manage.py", "migrate"])

# Criar admin
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@capyverb.com", "admin123")
    print("✅ Admin criado")

print("🚀 Iniciando servidor...")
import subprocess
subprocess.run(["gunicorn", "capyverb.wsgi:application", "--bind", "0.0.0.0:8080"])
'''
    
    with open('setup_postgres.py', 'w') as f:
        f.write(basic_script)
    
    print("✅ Script criado. Executando...")
    exec(basic_script)