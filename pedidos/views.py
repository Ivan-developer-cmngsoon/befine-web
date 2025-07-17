from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PedidoForm
from .models import DetallePedido
from carrito.models import ItemCarrito

@login_required
def realizar_pedido(request):
    usuario = request.user
    carrito = ItemCarrito.objects.filter(usuario=usuario)

    # 🔒 Validación: carrito vacío
    if not carrito.exists():
        messages.warning(request, "Tu carrito está vacío. Agrega productos antes de confirmar.")
        return redirect('ver_carrito')  # Asegúrate de que esta URL esté configurada

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
            return redirect('perfil_cliente')  # Luego cambiarás esto a historial si lo implementas
    else:
        form = PedidoForm()

    return render(request, 'pedidos/realizar_pedido.html', {'form': form})
