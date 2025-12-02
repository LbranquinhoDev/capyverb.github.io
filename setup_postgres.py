#!/usr/bin/env python
import os
import sys
import time
import psycopg2
from psycopg2 import OperationalError
import django

def wait_for_postgres(max_retries=30, delay=2):
    """Aguarda o PostgreSQL ficar disponível"""
    print("🔄 Aguardando PostgreSQL ficar disponível...")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada")
        return False
    
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(database_url)
            conn.close()
            print("✅ PostgreSQL conectado com sucesso!")
            return True
        except OperationalError as e:
            print(f"⏳ Tentativa {i+1}/{max_retries}: PostgreSQL ainda não disponível...")
            if i < max_retries - 1:
                time.sleep(delay)
    
    print("❌ PostgreSQL não ficou disponível a tempo")
    return False

def setup_database():
    """Configuração completa do banco"""
    print("=" * 60)
    print("🚀 CONFIGURAÇÃO DO POSTGRESQL NO RAILWAY")
    print("=" * 60)
    
    # 1. Aguardar PostgreSQL
    if not wait_for_postgres():
        return False
    
    # 2. Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
    django.setup()
    
    # 3. Aplicar migrações
    print("\n📦 Aplicando migrações Django...")
    from django.core.management import execute_from_command_line
    
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações aplicadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return False
    
    # 4. Criar superuser
    print("\n👑 Criando superuser...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        # Verificar se já existe
        if User.objects.filter(username='admin').exists():
            admin = User.objects.get(username='admin')
            print(f"✅ Admin já existe: {admin.username}")
            
            # Garantir permissões
            if not admin.is_superuser:
                admin.is_superuser = True
                admin.is_staff = True
                admin.save()
                print("✅ Admin promovido a superuser")
        else:
            # Criar novo
            User.objects.create_superuser(
                username='admin',
                email='admin@capyverb.com',
                password='admin123'
            )
            print("✅ SUPERUSER CRIADO: admin / admin123")
        
        # 5. Verificação
        print("\n🔍 VERIFICAÇÃO FINAL:")
        print(f"📊 Total de usuários: {User.objects.count()}")
        print(f"👑 Superusers: {User.objects.filter(is_superuser=True).count()}")
        
        users = User.objects.all()[:5]  # Mostrar primeiros 5
        for user in users:
            print(f"   👤 {user.username} | {user.email} | Superuser: {user.is_superuser}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar superuser: {e}")
        return False

def check_database_connection():
    """Verifica conexão e lista tabelas"""
    print("\n🔍 VERIFICANDO CONEXÃO E TABELAS...")
    
    database_url = os.getenv('DATABASE_URL')
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Listar todas as tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"📊 Tabelas no PostgreSQL: {len(tables)}")
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]}: {count} registros")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 INICIANDO CONFIGURAÇÃO COMPLETA DO POSTGRES")
    print("="*60)
    
    success = True
    
    # Verificar conexão
    if not check_database_connection():
        success = False
    
    # Setup completo
    if success and setup_database():
        print("\n" + "="*60)
        print("🎉 POSTGRES CONFIGURADO COM SUCESSO!")
        print("="*60)
        
        # Iniciar servidor
        print("\n🌐 INICIANDO SERVIDOR GUNICORN...")
        port = os.getenv('PORT', '8080')
        os.execvp("gunicorn", [
            "gunicorn",
            "capyverb.wsgi:application",
            "--bind", f"0.0.0.0:{port}",
            "--workers", "2"
        ])
    else:
        print("\n💥 FALHA NA CONFIGURAÇÃO DO POSTGRES")
        sys.exit(1)