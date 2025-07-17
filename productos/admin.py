from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre',)
