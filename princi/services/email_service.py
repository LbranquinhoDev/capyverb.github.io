
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template.loader import render_to_string



class EmailService:
    @staticmethod
    def enviar_email_convite(email, codigo_convite):
        subject = "🎉 Seu Convite para o Capyverb!"
        
        html_content = render_to_string('emails/convite.html', {
            'codigo': codigo_convite,
            'site_url': settings.SITE_URL
        })
        
        return EmailService._enviar_email(email, subject, html_content)
    
    @staticmethod
    def enviar_email_boas_vindas(usuario, senha_temporaria=None):
        subject = "🌟 Bem-vindo ao Capyverb!"
        
        html_content = render_to_string('emails/boas_vindas.html', {
            'usuario': usuario,
            'senha_temporaria': senha_temporaria,
            'site_url': settings.SITE_URL
        })
        
        return EmailService._enviar_email(usuario.email, subject, html_content)
    
    @staticmethod
    def _enviar_email(to_email, subject, html_content):
        try:
            
            message = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            
            print(f"✅ Email enviado para {to_email}. Status: {response.status_code}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {str(e)}")
            return False