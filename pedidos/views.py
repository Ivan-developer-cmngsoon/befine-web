from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import PedidoForm
from .models import DetallePedido, Pedido
from carrito.models import ItemCarrito
from productos.models import Producto
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now
from django.db.models import Q

@login_required
def realizar_pedido(request):
    usuario = request.user
    carrito = ItemCarrito.objects.filter(usuario=usuario)

    if not carrito.exists():
        messages.warning(request, "Tu carrito está vacío. Agrega productos antes de confirmar.")
        return redirect('ver_carrito')

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = usuario
            pedido.total = 0
            pedido.pagado = False
            pedido.estado = 'pendiente'
            pedido.save()

            total_pedido = 0
            for item in carrito:
                subtotal = item.subtotal()
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    subtotal=subtotal
                )
                total_pedido += subtotal

            pedido.total = total_pedido
            pedido.save()

            asunto = "Confirmación de tu pedido en Befine"
            contexto = {
                'nombre': usuario.first_name or usuario.username,
                'direccion': pedido.direccion,
                'comuna': pedido.comuna,
                'telefono': pedido.telefono,
                'total': pedido.total,
            }
            html_mensaje = render_to_string('pedidos/email_confirmacion.html', contexto)
            texto_mensaje = strip_tags(html_mensaje)
            send_mail(
                asunto,
                texto_mensaje,
                'tucorreo@gmail.com',
                [usuario.email],
                html_message=html_mensaje,
            )

            return redirect('simular_pago', pedido_id=pedido.id)
        else:
            print(form.errors)
    else:
        ultimo_pedido = Pedido.objects.filter(cliente=usuario).order_by('-fecha').first()
        form = PedidoForm(initial={
            'direccion': ultimo_pedido.direccion if ultimo_pedido else '',
            'comuna': ultimo_pedido.comuna if ultimo_pedido else '',
            'telefono': ultimo_pedido.telefono if ultimo_pedido else '',
        })

    return render(request, 'pedidos/realizar_pedido.html', {'form': form})

@login_required
def historial_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')
    return render(request, 'pedidos/historial.html', {'pedidos': pedidos})

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    detalles = pedido.detalles.all()
    return render(request, 'pedidos/detalle.html', {'pedido': pedido, 'detalles': detalles})

@login_required
def repetir_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    detalles = pedido.detalles.all()

    for item in detalles:
        producto = item.producto
        existente = ItemCarrito.objects.filter(usuario=request.user, producto=producto).first()
        if existente:
            existente.cantidad += item.cantidad
            existente.save()
        else:
            ItemCarrito.objects.create(
                usuario=request.user,
                producto=producto,
                cantidad=item.cantidad
            )

    messages.success(request, f"Los productos del pedido #{pedido.id} fueron añadidos a tu carrito.")
    return redirect('ver_carrito')

@login_required
def simular_pago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)

    if request.method == 'POST':
        pedido.pagado = True
        pedido.estado = 'pagado'
        pedido.metodo_pago = 'webpay'
        pedido.save()

        ItemCarrito.objects.filter(usuario=request.user).delete()

        messages.success(request, f'¡Pago realizado con éxito! Pedido #{pedido.id} confirmado.')
        return redirect('historial_pedidos')

    return render(request, 'pedidos/simular_pago.html', {'pedido': pedido})

# Verificación de rol admin/dueño
def es_admin(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['Administrador', 'Dueño']).exists())

@user_passes_test(es_admin)
def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado and nuevo_estado != pedido.estado:
            pedido.estado = nuevo_estado
            pedido.fecha_actualizacion_estado = now()
            pedido.save()
            messages.success(request, f'El estado del pedido #{pedido.id} fue actualizado a "{pedido.get_estado_display()}".')
        else:
            messages.info(request, f'El estado del pedido #{pedido.id} no fue modificado.')
    else:
        messages.warning(request, 'Acceso no válido.')

    return redirect('admin_pedidos')

@user_passes_test(es_admin)
def admin_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')

    estado = request.GET.get('estado')
    cliente = request.GET.get('cliente')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if estado:
        pedidos = pedidos.filter(estado=estado)
    if cliente:
        pedidos = pedidos.filter(cliente__username__icontains=cliente)
    if fecha_inicio:
        pedidos = pedidos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        pedidos = pedidos.filter(fecha__lte=fecha_fin)

    return render(request, 'pedidos/admin_pedidos_list.html', {
        'pedidos': pedidos,
        'filtro_estado': estado or '',
        'filtro_cliente': cliente or '',
        'filtro_fecha_inicio': fecha_inicio or '',
        'filtro_fecha_fin': fecha_fin or '',
    })
