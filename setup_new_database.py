import os
import django
import sys
import time
import psycopg2
from django.db import connection


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

def wait_for_database(max_retries=30, delay=2):
    """Aguarda o PostgreSQL ficar disponível"""
    print("🔄 Aguardando PostgreSQL ficar disponível...")
    
    for i in range(max_retries):
        try:
            # Tenta conectar com o banco
            connection.ensure_connection()
            print("✅ PostgreSQL conectado com sucesso!")
            return True
        except Exception as e:
            print(f"⏳ Tentativa {i+1}/{max_retries}: PostgreSQL ainda não disponível...")
            if i < max_retries - 1:
                time.sleep(delay)
    
    print("❌ PostgreSQL não ficou disponível a tempo")
    return False

def setup_new_database():
    """Configura um banco de dados completamente novo"""
    print("🔄 INICIANDO CONFIGURAÇÃO DO NOVO BANCO DE DADOS...")
    
    if not wait_for_database():
        return False
    
    print("📦 Aplicando migrações...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações aplicadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return False
    
    # 3. Criar superuser
    print("👑 Criando superuser...")
    User = get_user_model()
    
    try:
        # Verificar se já existe superuser
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser já existe no sistema")
        else:
            # Criar novo superuser
            admin = User.objects.create_superuser(
                username='capyadmins',
            email='adminscapy@capyverb.com',
            password='capyadmins$'
            )
            print("✅ Superuser criado: admin / admin123")
            
            # Verificar criação
            user_count = User.objects.count()
            superuser_count = User.objects.filter(is_superuser=True).count()
            
            print(f"📊 Estatísticas do banco:")
            print(f"   • Total de usuários: {user_count}")
            print(f"   • Superusers: {superuser_count}")
            
    except Exception as e:
        print(f"❌ Erro ao criar superuser: {e}")
        # Tentar método alternativo
        return create_superuser_alternative()
    
    print("🎉 CONFIGURAÇÃO DO BANCO CONCLUÍDA COM SUCESSO!")
    return True

def create_superuser_alternative():
    """Método alternativo para criar superuser"""
    print("🔄 Tentando método alternativo para criar superuser...")
    try:
        from django.contrib.auth.management.commands.createsuperuser import Command
        from io import StringIO
        
        # Simula o comando createsuperuser
        cmd = Command()
        cmd.stdout = StringIO()
        
        # Cria superuser diretamente
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='capyadmins',
            email='adminscapy@capyverb.com',
            password='capyadmins$'
            )
            print("✅ Superuser criado via método alternativo")
        return True
    except Exception as e:
        print(f"❌ Erro no método alternativo: {e}")
        return False

if __name__ == "__main__":
    success = setup_new_database()
    if success:
        print("🚀 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        sys.exit(0)
    else:
        print("💥 FALHA NA CONFIGURAÇÃO DO BANCO")
        sys.exit(1)