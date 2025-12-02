import os
import sys
import time


#Forçar variaveis de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')

#Importar Django
try:
    import django
    django.setup()
except Exception as e:
    print(f"Erro ao configurar Django: {e}")
    sys.exit(1)

# Aplicar migrações

try:
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])

except Exception as e:
    print(f"Erro nas migrações: {e}")

# CRIAR SUPERUSER 

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    
    from django.db import connection
    connection.ensure_connection()
    
    # Metodo 1: Verificar se ja existe
    if User.objects.filter(username='admin').exists():
        user = User.objects.get(username='admin')
        print(f" Admin já existe: {user.username}")
        
        # Garantir que é superuser
        if not user.is_superuser or not user.is_staff:
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print("Admin promovido a superuser/staff")
    else:
        # Método 2: Criar novo
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@capyverb.com',
                password='admin123'
            )

        except Exception as e:
            print(f"Erro ao criar superuser (método 1): {e}")
            
            # Método 3: Criar manualmente
            try:
                user = User.objects.create_user(
                    username='admin',
                    email='admin@capyverb.com',
                    password='admin123'
                )
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print("SUPERUSER CRIADO (metodo manual)")
            except Exception as e2:
                print(f"Erro ao criar superuser (metodo 2): {e2}")
    
    # VERIFICAÇÃO FINAL
    all_users = User.objects.all()
    print(f"Total de usuários: {all_users.count()}")
    
    for user in all_users:
        print(f" {user.username} | {user.email} | Superuser: {user.is_superuser} | Staff: {user.is_staff}")
    
except Exception as e:
    print(f"ERRO CRÍTICO: {e}")
    import traceback
    traceback.print_exc()

# INICIAR SERVIDOR

port = os.getenv('PORT', '8080')
os.execvp("gunicorn", [
    "gunicorn",
    "capyverb.wsgi:application",
    "--bind", f"0.0.0.0:{port}",
    "--workers", "1",
    "--timeout", "120"
])