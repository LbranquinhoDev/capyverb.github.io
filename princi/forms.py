# princi/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Convite

class CadastroComConviteForm(UserCreationForm):
    codigo_convite = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-5',
            'placeholder': 'Código do convite'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control rounded-5',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-5',
            'placeholder': 'Nome de usuário'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control rounded-5',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control rounded-5',
            'placeholder': 'Confirmar senha'
        })

    def clean(self):
        cleaned_data = super().clean()
        codigo_convite = cleaned_data.get('codigo_convite')
        email = cleaned_data.get('email')
        
        # Verificar se o convite existe e é válido
        try:
            convite = Convite.objects.get(
                codigo=codigo_convite, 
                email=email, 
                usado=False
            )
        except Convite.DoesNotExist:
            raise forms.ValidationError("Convite inválido ou já utilizado!")
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-5',
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-5', 
            'placeholder': 'Senha'
        })
    )