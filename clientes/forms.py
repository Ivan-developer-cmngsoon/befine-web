from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PerfilCliente

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este correo ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data
class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = ['direccion', 'comuna', 'telefono', 'referencia']
        labels = {
            'direccion': 'Dirección',
            'comuna': 'Comuna',
            'telefono': 'Teléfono',
            'referencia': 'Referencia (opcional)',
        }