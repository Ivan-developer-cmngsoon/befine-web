from django.shortcuts import render
from .models import Producto

def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'productos/lista.html', {'productos': productos})
