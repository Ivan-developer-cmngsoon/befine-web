from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistroForm, PerfilUsuarioForm
from .models import PerfilUsuario


@login_required
def perfil_cliente(request):
    tiene_perfil = hasattr(request.user, 'perfilusuario')
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
    perfil, creado = PerfilUsuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil_cliente')
    else:
        form = PerfilUsuarioForm(instance=perfil)

    return render(request, 'clientes/completar_perfil.html', {'form': form})
