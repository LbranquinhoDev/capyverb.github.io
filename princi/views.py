
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CadastroComConviteForm, LoginForm
from .models import Convite


def is_admin(user):
    return user.is_staff

def index(request):
    return render(request, 'princi/index.html')

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroComConviteForm(request.POST)
        if form.is_valid():
            
            codigo_convite = form.cleaned_data['codigo_convite']
            email = form.cleaned_data['email']
            
            convite = Convite.objects.get(
                codigo=codigo_convite, 
                email=email, 
                usado=False
            )
            
            
            user = form.save()
            
            
            convite.usado = True
            convite.usuario = user
            convite.save()
            
            
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = LoginForm()
    
    return render(request, 'princi/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você foi desconectado.')
    return redirect('index')

@login_required
@user_passes_test(is_admin)
def admin_convites(request):
    if request.method == 'POST':
        emails = request.POST.get('emails', '').split('\n')
        for email in emails:
            email = email.strip()
            if email:
                Convite.objects.get_or_create(email=email)
        messages.success(request, f'{len(emails)} convites criados!')
    
    convites = Convite.objects.all().order_by('-data_criacao')
    return render(request, 'princi/admin_convites.html', {'convites': convites})

@login_required
@user_passes_test(is_admin) 
def enviar_convite(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    # Integrar com serviço de email aqui
    # por enquanto, apenas uma mensagem de sucesso
    messages.info(request, f'Convite para {convite.email}: {convite.codigo}')
    return redirect('admin_convites')

def aulas(request):
    return render(request, 'princi/aulas.html')


def verificar_admin(user):
    """Verifica se o usuário é admin/staff"""
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(verificar_admin, login_url='/login/')
def admin_convites(request):

    if not request.user.is_authenticated:
        messages.warning(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login')
    
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito para administradores.')
        return redirect('index')
    
    if request.method == 'POST':
        emails = request.POST.get('emails', '').split('\n')
        convites_criados = 0
        for email in emails:
            email = email.strip()
            if email:
                convite, created = Convite.objects.get_or_create(email=email)
                if created:
                    convites_criados += 1
        messages.success(request, f'{convites_criados} convites criados!')
        return redirect('admin_convites')
    
    convites = Convite.objects.all().order_by('-data_criacao')
    return render(request, 'princi/admin_convites.html', {'convites': convites})
