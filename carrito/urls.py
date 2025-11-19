from django.urls import path
from . import views
from pedidos.views import realizar_pedido

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('aumentar/<int:item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir/<int:item_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path("modal/", views.ver_carrito_modal, name="ver_carrito_modal"),
]

