from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    address = models.CharField('Endereço', max_length=255, blank=True)
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('Estado', max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil do Cliente'
        verbose_name_plural = 'Perfis de Clientes'
        ordering = ['id']

    def __str__(self):
        return self.user.username