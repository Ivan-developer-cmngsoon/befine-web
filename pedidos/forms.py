from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion', 'comuna', 'telefono', 'detalle']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'direccion': 'Dirección de entrega',
            'comuna': 'Comuna',
            'telefono': 'Teléfono de contacto',
            'detalle': 'Detalles del pedido (opcional)',
        }
