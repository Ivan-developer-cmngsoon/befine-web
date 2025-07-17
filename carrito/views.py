from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import ItemCarrito
from django.contrib import messages

@login_required
def ver_carrito(request):
    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, 'carrito/ver_carrito.html', {'items': items, 'total': total})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    item, creado = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    if not creado:
        item.cantidad += 1
        item.save()
        messages.info(request, f'Se aumentó la cantidad de "{producto.nombre}" en tu carrito.')
    else:
        messages.success(request, f'"{producto.nombre}" fue agregado a tu carrito.')
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    messages.warning(request, f'"{item.producto.nombre}" fue eliminado del carrito.')
    item.delete()
    return redirect('ver_carrito')
