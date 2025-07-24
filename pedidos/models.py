from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from productos.models import Producto


class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    detalle = models.TextField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_actualizacion_estado = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.username}'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'