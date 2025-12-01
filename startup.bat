@echo off
echo 🚀 INICIANDO DEPLOY NO RAILWAY...

echo 📦 Aplicando migrações...
python manage.py migrate

echo 👑 Criando superuser...
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Verifica se existe algum superuser
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print('✅ Superusers existentes:')
    for user in superusers:
        print('   -', user.username, '(', user.email, ')')
else:
    print('❌ Nenhum superuser encontrado. Criando...')
    try:
        User.objects.create_superuser('admin', 'admin@capyverb.com', 'admin123')
        print('✅ SUPERUSER CRIADO: admin / admin123')
    except Exception as e:
        print('💥 Erro ao criar superuser:', e)
        # Tentativa alternativa
        try:
            User.objects.create_user('admin', 'admin@capyverb.com', 'admin123', is_superuser=True, is_staff=True)
            print('✅ SUPERUSER CRIADO (metodo alternativo)')
        except Exception as e2:
            print('💥 Erro no metodo alternativo:', e2)
"

echo 🔍 Verificacao final...
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

users = User.objects.all()
print('📊 TOTAL DE USUARIOS:', users.count())
for user in users:
    print('   👤', user.username, '|', user.email, '| Superuser:', user.is_superuser)
"

echo 🌐 Iniciando servidor...
gunicorn capyverb.wsgi:application --bind 0.0.0.0:%PORT%