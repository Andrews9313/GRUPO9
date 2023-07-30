from django.contrib import admin
from .models import Asiento, Cliente, DetalleVenta, MetodoPago, Pelicula, Promocion, Sala, Ticket, Vendedor, Venta, Categoria,  Cartelera, Horario, Presentacion

# Register your models here.
admin.site.register(Asiento),
admin.site.register(Cliente),
# admin.site.register(DetallePromocion),
admin.site.register(DetalleVenta),
admin.site.register(MetodoPago),
admin.site.register(Pelicula),
admin.site.register(Sala),
admin.site.register(Ticket),
admin.site.register(Vendedor),
admin.site.register(Venta),
admin.site.register(Promocion),
admin.site.register(Categoria),
admin.site.register(Cartelera),
admin.site.register(Horario),
admin.site.register(Presentacion),

