from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto  # Asegúrate de tener esta app y modelo

class ItemCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    agregado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} ({self.usuario.username})'

    def subtotal(self):
        return self.producto.precio * self.cantidad
