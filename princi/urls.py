
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('aulas/', views.aulas, name='aulas'),
    path('painel/convites/', views.admin_convites, name='admin_convites'),
    path('painel/excluir-usuario/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('painel/alterar-cargo/<int:user_id>/', views.alterar_cargo, name='alterar_cargo'),
    path('painel/enviar-convite/<int:convite_id>/', views.enviar_convite, name='enviar_convite'),
]