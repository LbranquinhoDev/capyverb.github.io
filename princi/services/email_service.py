import resend
from django.conf import settings
from django.template.loader import render_to_string
import os

# Configuração do Resend
resend.api_key = getattr(settings, 'RESEND_API_KEY', os.environ.get('RESEND_API_KEY'))

class EmailService:
    @staticmethod
    def enviar_email_convite(email, codigo_convite):
        subject = "🎉 Seu Convite para o Capyverb!"
        
        html_content = render_to_string('emails/convite.html', {
            'codigo': codigo_convite,
            'site_url': settings.SITE_URL
        })
        
        return EmailService._enviar_email_inteligente(email, subject, html_content)
    
    @staticmethod
    def enviar_email_boas_vindas(usuario, senha_temporaria=None):
        subject = "🌟 Bem-vindo ao Capyverb!"
        
        html_content = render_to_string('emails/boas_vindas.html', {
            'usuario': usuario,
            'senha_temporaria': senha_temporaria,
            'site_url': settings.SITE_URL
        })
        
        return EmailService._enviar_email_inteligente(usuario.email, subject, html_content)
    
    @staticmethod
    def _enviar_email_inteligente(to_email, subject, html_content):
        # MODO DESENVOLVIMENTO: Mostra no console
        if settings.DEBUG:
            print("=" * 60)
            print("📧 EMAIL SIMULAÇÃO (Desenvolvimento)")
            print(f"De: Capyverb <{settings.DEFAULT_FROM_EMAIL}>")
            print(f"Para: {to_email}")
            print(f"Assunto: {subject}")
            print("🔗 Link de cadastro:", f"{settings.SITE_URL}/cadastro/{'CODIGO_EXEMPLO'}")
            print("=" * 60)
            return True
        
        # MODO PRODUÇÃO: Envia email real
        try:
            # Para produção, use um from address que funcione
            from_email = "Capyverb <capyverb@resend.dev>"
            
            params = {
                "from": from_email,
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }
            
            print(f"🚀 Enviando email real para: {to_email}")
            email = resend.Emails.send(params)
            print(f"✅ Email enviado com sucesso! ID: {email['id']}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {str(e)}")
            
            # Fallback: mostra no console mesmo em produção se der erro
            print("🔄 Usando fallback console devido ao erro:")
            print(f"Para: {to_email}")
            print(f"Assunto: {subject}")
            return False