from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PedidoForm
from .models import DetallePedido, Pedido
from carrito.models import ItemCarrito
from productos.models import Producto


@login_required
def realizar_pedido(request):
    usuario = request.user
    carrito = ItemCarrito.objects.filter(usuario=usuario)

    # 🔒 Validación: carrito vacío
    if not carrito.exists():
        messages.warning(request, "Tu carrito está vacío. Agrega productos antes de confirmar.")
        return redirect('ver_carrito')

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # 🧾 Guardar información del pedido (sin total aún)
            pedido = form.save(commit=False)
            pedido.cliente = usuario
            pedido.total = 0  # Se actualizará después
            pedido.save()

            total_pedido = 0

            # 🧺 Crear detalle por cada ítem del carrito
            for item in carrito:
                subtotal = item.subtotal()
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    subtotal=subtotal
                )
                total_pedido += subtotal

            # 💰 Actualizar total real del pedido
            pedido.total = total_pedido
            pedido.save()

            # 🧹 Vaciar el carrito
            carrito.delete()

            messages.success(request, f'Pedido #{pedido.id} confirmado con éxito.')
            return redirect('perfil_cliente')  # Puedes cambiar esto a 'historial_pedidos' si ya lo usas
    else:
        # 🧠 Precargar datos del último pedido si existen
        ultimo_pedido = Pedido.objects.filter(cliente=usuario).order_by('-fecha').first()
        if ultimo_pedido:
            form = PedidoForm(initial={
                'direccion': ultimo_pedido.direccion,
                'comuna': ultimo_pedido.comuna,
                'telefono': ultimo_pedido.telefono,
                'detalle': ''
            })
        else:
            form = PedidoForm()

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
        # Busca si ya existe en el carrito
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
