from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistroForm, PerfilUsuarioForm
from .models import PerfilUsuario

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Enviar correo de bienvenida
            contexto = {
                'nombre': user.first_name or user.username,
            }
            html_mensaje = render_to_string('clientes/email_bienvenida.html', contexto)
            texto_mensaje = strip_tags(html_mensaje)

            send_mail(
                "Bienvenido a Befine 💧",
                texto_mensaje,
                'tucorreo@gmail.com',  # Usa DEFAULT_FROM_EMAIL si prefieres
                [user.email],
                html_message=html_mensaje,
            )

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'clientes/registro.html', {'form': form})