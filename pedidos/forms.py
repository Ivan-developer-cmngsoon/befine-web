from django import forms
from .models import Pedido
from django.core.validators import RegexValidator

class PedidoForm(forms.ModelForm):
    telefono = forms.CharField(
        label="Teléfono de contacto",
        max_length=20,
        validators=[RegexValidator(r'^\+?[\d\s\-]{9,}$', message="Ingresa un teléfono válido.")],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +569 1234 5678'})
    )

    class Meta:
        model = Pedido
        fields = ['direccion', 'comuna', 'telefono', 'detalle']
        widgets = {
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle y número, depto si aplica'
            }),
            'comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Quilicura'
            }),
            'detalle': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Instrucciones especiales de entrega (opcional)',
                'rows': 3
            }),
        }
        labels = {
            'direccion': 'Dirección de entrega',
            'comuna': 'Comuna',
            'detalle': 'Detalles del pedido (opcional)',
        }

    def clean_direccion(self):
        data = self.cleaned_data['direccion']
        if len(data.strip()) < 5:
            raise forms.ValidationError("La dirección es demasiado corta.")
        return data

    def clean_comuna(self):
        data = self.cleaned_data['comuna']
        if len(data.strip()) < 3:
            raise forms.ValidationError("Debes ingresar una comuna válida.")
        return data
