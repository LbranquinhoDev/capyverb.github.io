from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CadastroComConviteForm, LoginForm
from .models import Convite
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import secrets
from django.http import HttpResponse
from django.db import connection
import os



def is_admin(user):
    return user.is_staff


def index(request):
    return render(request, 'princi/index.html')


def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroComConviteForm(request.POST)
        if form.is_valid():
            # Pega dados do formulario
            codigo_convite = form.cleaned_data['codigo_convite']
            email = form.cleaned_data['email']
            
            # Busca convite valido no banco
            convite = Convite.objects.get(
                codigo=codigo_convite, 
                email=email, 
                usado=False
            )
            
            # Cria novo usuario
            user = form.save()
            
            # Marca convite como usado
            convite.usado = True
            convite.usuario = user
            convite.save()
            
            # Faz login automatico
            login(request, user)
            messages.success(request, 'Cadastro feito!')
            return redirect('index')
    else:
        form = CadastroComConviteForm()
    
    return render(request, 'princi/cadastro.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid():
            # Autentica usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Login bem sucedido
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('index')
            else:
                
                messages.error(request, 'Usuario ou senha invalidos.')
        else:
            # Formulario invalido
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = LoginForm()
    
    return render(request, 'princi/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Voce foi desconectado.')
    return redirect('index')


def aulas(request):
    return render(request, 'princi/aulas.html')


@login_required
@user_passes_test(is_admin)
def admin_convites(request):
    try:
        
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito para administradores.')
            return redirect('index')
        
        # Processa criacao de convites via POST
        if request.method == 'POST':
            emails = request.POST.get('emails', '').split('\n')
            convites_criados = 0
            
            # Cria convites para cada email
            for email in emails:
                email = email.strip()
                if email:
                    # Cria convite se nao existir
                    convite, created = Convite.objects.get_or_create(
                        email=email,
                        defaults={'usado': False}
                    )
                    if created:
                        convites_criados += 1
                        print(f"Convite criado: {convite.email} - {convite.codigo}")
            
            
            if convites_criados > 0:
                messages.success(request, f'{convites_criados} convites criados com sucesso!')
            else:
                messages.info(request, 'Nenhum novo convite criado (ja existiam)')
            
            return redirect('admin_convites')
        
        
        convites = Convite.objects.all().order_by('-data_criacao')
        usuarios = User.objects.all().order_by('-date_joined')
        
        
        context = {
            'convites': convites,
            'usuarios': usuarios,
        }
        
        return render(request, 'princi/admin_convites.html', context)
    
    except Exception as e:
        print(f"ERRO em admin_convites: {str(e)}")
        messages.error(request, f'Erro ao processar: {str(e)}')
        return redirect('admin_convites')
    
    

@login_required
@user_passes_test(is_admin) 
def enviar_convite(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    # Por enquanto so mostra codigo do convite
    messages.info(request, f'Convite para {convite.email}: {convite.codigo}')
    return redirect('admin_convites')


@login_required
def excluir_usuario(request, user_id):
    # So superusuario pode excluir
    if not request.user.is_superuser:
        messages.error(request, 'Voce nao tem permissao para executar esta acao.')
        return redirect('admin_convites')
    
    usuario = get_object_or_404(User, id=user_id)
    
    # Impede auto exclusao
    if usuario == request.user:
        messages.error(request, 'Voce nao pode excluir sua propria conta.')
        return redirect('admin_convites')
    
    
    usuario.delete()
    messages.success(request, 'Usuario excluido com sucesso!')
    return redirect('admin_convites')


@login_required
def alterar_cargo(request, user_id):
    
    if not request.user.is_superuser:
        messages.error(request, 'Sem permissao para esta acao')
        return redirect('admin_convites')
    
    # Busca usuario alvo
    usuario = get_object_or_404(User, id=user_id)
    
    
    if usuario == request.user:
        messages.error(request, 'Nao pode mudar seu proprio cargo!')
        return redirect('admin_convites')
    
    # Alterna entre staff e nao staff
    if usuario.is_staff:
        
        usuario.is_staff = False
        messages.success(request, f'{usuario.username} agora e usuario normal!')
    else:
        # Adiciona privilegios de admin
        usuario.is_staff = True
        messages.success(request, f'{usuario.username} agora e administrador!')
    
    
    usuario.save()
    
    
    return redirect('admin_convites')


def criar_convites(request):
    if request.method == 'POST':
        emails = request.POST.get('emails', '').split('\n')
        emails_criados = 0
        
        for email in emails:
            email = email.strip()
            if email:
                # Criar convite
                codigo = secrets.token_urlsafe(8)
                convite = Convite.objects.create(email=email, codigo=codigo)
                emails_criados += 1
        
        messages.success(request, f'{emails_criados} convites criados!')

def cadastro_com_convite(request, codigo):
    
    convite = get_object_or_404(Convite, codigo=codigo, usado=False)
    
    if request.method == 'POST':
        #codigo de criação de usuário
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Criar usuário
            novo_usuario = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Marcar convite como usado
            convite.usado = True
            convite.usuario = novo_usuario
            convite.save()
            
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}')
    

    return render(request, 'princi/cadastro.html', {'codigo': codigo, 'convite': convite})
