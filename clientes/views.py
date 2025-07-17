from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistroForm

@login_required
def perfil_cliente(request):
    return render(request, 'clientes/perfil.html')

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