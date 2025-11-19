from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from productos.models import Producto
from .models import ItemCarrito

# --- Helper reutilizable ---
def _carrito_items_y_total(user):
    # select_related para evitar N+1 al acceder a producto
    items = ItemCarrito.objects.filter(usuario=user).select_related('producto')
    # Asume que tu modelo tiene item.subtotal() -> num
    total = sum(item.subtotal() for item in items)
    return items, total

@login_required
def ver_carrito(request):
    items, total = _carrito_items_y_total(request.user)
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

    # Redirige a la misma página donde estaba el usuario
    return redirect(request.META.get('HTTP_REFERER', 'ver_carrito'))

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    messages.warning(request, f'"{item.producto.nombre}" fue eliminado del carrito.')
    item.delete()
    return redirect('ver_carrito')

# --- NUEVO: contenido del carrito para modal (AJAX) ---
@login_required
def ver_carrito_modal(request):
    # Recomendado: aceptar solo solicitudes AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return HttpResponseBadRequest('Esta ruta es solo para solicitudes AJAX.')

    items, total = _carrito_items_y_total(request.user)
    # Este template será el partial que crearemos a continuación
    return render(request, 'carrito/_modal_contenido.html', {
        'items': items,
        'total': total,
    })

@login_required
def aumentar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    item.cantidad += 1
    item.save()
    return redirect(request.META.get('HTTP_REFERER', 'ver_carrito'))

@login_required
def disminuir_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'ver_carrito'))
