from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CadastroComConviteForm, LoginForm
from .models import Convite
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .services.email_service import EmailService
import secrets

# Funcao para verificar se usuario e admin
def is_admin(user):
    return user.is_staff

# Pagina inicial do site
def index(request):
    return render(request, 'princi/index.html')

# View para cadastro de usuarios com convite
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


# View para login de usuarios
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
                # Credenciais invalidas
                messages.error(request, 'Usuario ou senha invalidos.')
        else:
            # Formulario invalido
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = LoginForm()
    
    return render(request, 'princi/login.html', {'form': form})

# View para logout
def logout_view(request):
    logout(request)
    messages.info(request, 'Voce foi desconectado.')
    return redirect('index')

# Pagina de aulas
def aulas(request):
    return render(request, 'princi/aulas.html')

# Painel administrativo - so para admins
@login_required
@user_passes_test(is_admin)
def admin_convites(request):
    try:
        # Verifica se usuario tem permissao
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
            
            # Mensagem de feedback
            if convites_criados > 0:
                messages.success(request, f'{convites_criados} convites criados com sucesso!')
            else:
                messages.info(request, 'Nenhum novo convite criado (ja existiam)')
            
            return redirect('admin_convites')
        
        # Busca dados para exibir
        convites = Convite.objects.all().order_by('-data_criacao')
        usuarios = User.objects.all().order_by('-date_joined')
        
        # Prepara contexto para template
        context = {
            'convites': convites,
            'usuarios': usuarios,
        }
        
        return render(request, 'princi/admin_convites.html', context)
    
    except Exception as e:
        # Tratamento de erro generico
        print(f"ERRO em admin_convites: {str(e)}")
        messages.error(request, f'Erro ao processar: {str(e)}')
        return redirect('admin_convites')
    
    
# View para enviar convite (simulacao)
@login_required
@user_passes_test(is_admin) 
def enviar_convite(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    # Por enquanto so mostra codigo do convite
    messages.info(request, f'Convite para {convite.email}: {convite.codigo}')
    return redirect('admin_convites')

# View para excluir usuario
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
    
    # Exclui usuario
    usuario.delete()
    messages.success(request, 'Usuario excluido com sucesso!')
    return redirect('admin_convites')

# View para alterar cargo de usuario
@login_required
def alterar_cargo(request, user_id):
    # So superusuario pode alterar cargos
    if not request.user.is_superuser:
        messages.error(request, 'Sem permissao para esta acao')
        return redirect('admin_convites')
    
    # Busca usuario alvo
    usuario = get_object_or_404(User, id=user_id)
    
    # Impede auto alteracao
    if usuario == request.user:
        messages.error(request, 'Nao pode mudar seu proprio cargo!')
        return redirect('admin_convites')
    
    # Alterna entre staff e nao staff
    if usuario.is_staff:
        # Remove privilegios de admin
        usuario.is_staff = False
        messages.success(request, f'{usuario.username} agora e usuario normal!')
    else:
        # Adiciona privilegios de admin
        usuario.is_staff = True
        messages.success(request, f'{usuario.username} agora e administrador!')
    
    # Salva alteracao no banco
    usuario.save()
    
    # Retorna para painel
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
                
                # Enviar email
                if EmailService.enviar_email_convite(email, codigo):
                    emails_criados += 1
        
        messages.success(request, f'{len(emails)} convites criados! {emails_criados} emails enviados.')
        
def cadastro_com_convite(request, codigo):
    # Sua lógica completa de cadastro aqui
    convite = get_object_or_404(Convite, codigo=codigo, usado=False)
    
    if request.method == 'POST':
        # Seu código de criação de usuário
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
            
            # Enviar email de boas-vindas
            EmailService.enviar_email_boas_vindas(novo_usuario)
            
            messages.success(request, 'Conta criada com sucesso! Verifique seu email para as boas-vindas.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}')
    
    # Renderizar template de cadastro
    return render(request, 'princi/cadastro.html', {'codigo': codigo, 'convite': convite})