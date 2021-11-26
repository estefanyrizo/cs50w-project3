from django.contrib import admin
from .models import Categoria, Extra, Platillo, Pedido, DetallePedido

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Extra)
admin.site.register(Platillo)
admin.site.register(Pedido)
admin.site.register(DetallePedido)