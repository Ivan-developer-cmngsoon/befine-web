from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROLES = [
        ('cliente', 'Cliente'),
        ('repartidor', 'Repartidor'),
        ('admin', 'Administrador'),
        ('dueno', 'Dueño'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    referencia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display})"
