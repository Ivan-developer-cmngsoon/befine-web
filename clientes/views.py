from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
    """
    Registro de nuevo usuario + envío de correo de bienvenida.
    """
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
                'tucorreo@gmail.com',  # idealmente usar DEFAULT_FROM_EMAIL
                [user.email],
                html_message=html_mensaje,
            )

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            # IMPORTANTE: usamos el namespace 'clientes'
            return redirect('clientes:login')
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
            # También mejor usar el namespace aquí
            return redirect('clientes:perfil_cliente')
    else:
        form = PerfilUsuarioForm(instance=perfil)

    return render(request, 'clientes/completar_perfil.html', {'form': form})
