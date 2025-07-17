from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistroForm, PerfilClienteForm  # IMPORTAMOS el nuevo formulario
from .models import PerfilCliente  # IMPORTAMOS el nuevo modelo


@login_required
def perfil_cliente(request):
    tiene_perfil = hasattr(request.user, 'perfilcliente')
    return render(request, 'clientes/perfil.html', {'tiene_perfil': tiene_perfil})


def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'clientes/registro.html', {'form': form})


@login_required
def completar_perfil(request):
    try:
        perfil = request.user.perfilcliente
    except PerfilCliente.DoesNotExist:
        perfil = None

    if request.method == 'POST':
        form = PerfilClienteForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
            return redirect('perfil_cliente')
    else:
        form = PerfilClienteForm(instance=perfil)

    return render(request, 'clientes/completar_perfil.html', {'form': form})
