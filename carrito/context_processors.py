from .models import ItemCarrito

def carrito_count(request):
    if request.user.is_authenticated:
        total_items = ItemCarrito.objects.filter(usuario=request.user).count()
    else:
        total_items = 0
    return {'carrito_count': total_items}
