from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
    ('recargas', 'Recargas'),
    ('dispensadores', 'Dispensadores'),
    ('accesorios', 'Accesorios'),
    ('Promociones', 'Pack Inicial')
        ]


    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
