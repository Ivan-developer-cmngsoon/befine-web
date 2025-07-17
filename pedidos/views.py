from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PedidoForm

@login_required
def realizar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user
            pedido.total = 0  # Temporal
            pedido.save()
            messages.success(request, 'Pedido realizado con éxito.')
            return redirect('perfil_cliente')
    else:
        form = PedidoForm()
    return render(request, 'pedidos/realizar_pedido.html', {'form': form})
