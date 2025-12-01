import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    
    # Verifica se já existe
    if User.objects.filter(username='admin').exists():
        print("✅ Usuário admin já existe")
        return True
    
    try:
        # Cria superuser
        User.objects.create_superuser(
            username='capyadmins',
            email='adminscapy@capyverb.com',
            password='capyadmins$'
        )
        print("✅ SUPERUSER CRIADO: admin / admin123")
        
        # Verifica
        users = User.objects.all()
        print(f"📊 Total de usuários: {users.count()}")
        for user in users:
            print(f"   - {user.username} (superuser: {user.is_superuser})")
            
        return True
    except Exception as e:
        print(f"❌ Erro ao criar superuser: {e}")
        return False

if __name__ == "__main__":
    create_admin()