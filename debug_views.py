import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capyverb.settings')
django.setup()

print("🔍 TESTANDO VIEWS DO DJANGO")
print("=" * 50)

# Importar todas as views para ver se há erros
try:
    from princi import views
    print("✅ Módulo views importado")
    
    # Listar todas as funções no views
    import inspect
    view_functions = []
    
    for name, obj in inspect.getmembers(views):
        if inspect.isfunction(obj) and not name.startswith('_'):
            view_functions.append(name)
    
    print(f"📋 Views encontradas: {len(view_functions)}")
    for view in sorted(view_functions):
        print(f"   • {view}")
        
except Exception as e:
    print(f"❌ Erro ao importar views: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("✅ DIAGNÓSTICO CONCLUÍDO")