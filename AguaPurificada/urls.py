from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),           # Home, contacto, etc.
    path('productos/', include('productos.urls')),
    path("clientes/", include(("clientes.urls", "clientes"), namespace="clientes")),
    path('pedidos/', include('pedidos.urls')),
    path('carrito/', include('carrito.urls')),
]

# Soporte para mostrar imágenes (solo en desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
