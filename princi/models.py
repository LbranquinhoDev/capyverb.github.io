
from django.db import models
from django.contrib.auth.models import User
import secrets

class Convite(models.Model):
    email = models.EmailField(unique=True)
    codigo = models.CharField(max_length=50, unique=True)
    usado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_uso = models.DateTimeField(null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def gerar_codigo(self):
        return secrets.token_urlsafe(16)
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.gerar_codigo()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.email} - {self.codigo}"