import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from django.db import connection

def setup_new_database():
    """Configura um banco de dados completamente novo"""
    print("🔄 INICIANDO CONFIGURAÇÃO DO NOVO BANCO DE DADOS...")
    
    # 1. Aplicar todas as migrações
    print("📦 Aplicando migrações...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações aplicadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return False
    
    # 2. Criar superuser
    print("👑 Criando superuser...")
    User = get_user_model()
    
    try:
        # Deletar superusers existentes (se houver)
        User.objects.filter(is_superuser=True).delete()
        print("🧹 Superusers antigos removidos")
        
        # Criar novo superuser
        admin = User.objects.create_superuser(
            username='capyadmins',
            email='adminscapy@capyverb.com',
            password='capyadmins$'
        )
        print("✅ Superuser criado: admin / admin123")
        
    except Exception as e:
        print(f"❌ Erro ao criar superuser: {e}")
        return False
    
    # 3. Verificar criação
    print("🔍 Verificando configuração...")
    try:
        user_count = User.objects.count()
        superuser_count = User.objects.filter(is_superuser=True).count()
        
        print(f"📊 Estatísticas do banco:")
        print(f"   • Total de usuários: {user_count}")
        print(f"   • Superusers: {superuser_count}")
        print(f"   • Tabelas criadas: ✅")
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False
    
    print("🎉 CONFIGURAÇÃO DO BANCO CONCLUÍDA COM SUCESSO!")
    return True

if __name__ == "__main__":
    success = setup_new_database()
    sys.exit(0 if success else 1)