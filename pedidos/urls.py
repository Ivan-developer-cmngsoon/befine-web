from django.urls import path
from . import views

urlpatterns = [
    path('realizar/', views.realizar_pedido, name='realizar_pedido'),
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
    path('detalle/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('repetir/<int:pedido_id>/', views.repetir_pedido, name='repetir_pedido'),
    path('pago/<int:pedido_id>/', views.simular_pago, name='simular_pago'),
    path('admin/actualizar-estado/<int:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('admin/', views.admin_pedidos, name='admin_pedidos'),
]
