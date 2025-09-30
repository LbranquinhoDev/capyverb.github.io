
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('aulas/', views.aulas, name='aulas'),
    path('painel/convites/', views.admin_convites, name='admin_convites'),
    path('painel/convites/<int:convite_id>/enviar/', views.enviar_convite, name='enviar_convite'),
]