from django.db import models
from django.db.models import ForeignKey
from autenticacion.models import Usuario
from django.utils.timezone import now

# Create your models here.
class Cliente(models.Model):
    objects = None
    nombre = models.CharField(max_length=225)
    apellido = models.CharField(max_length=225)
    email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_creacion", null=True)
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario_modificacion", null=True)

    class Meta:
        db_table = "Cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['fecha_creacion', 'apellido']

    def __str__(self):
        return '{}{}'.format(self.apellido, self.nombre)


class Venta(models.Model):
    objects = None
    cliente = ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    cantidad_ticket = models.IntegerField(blank=True, null=True)
    precio_unitario = models.IntegerField(default=1)
    total_venta_ticket = models.IntegerField(default=1)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Venta"
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        ordering = ['fecha_creacion', 'total_venta_ticket']

    def __str__(self):
        return '{}'.format(self.total_venta_ticket)


class MetodoPago(models.Model):
    objects = None
    descripcion = models.CharField(max_length=255)
    tipago = models.CharField(max_length=225)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "MetodoPago"
        verbose_name = "metodopago"
        verbose_name_plural = "metodospagos"
        ordering = ['fecha_creacion', 'tipago']

    def __str__(self):
        return '{}'.format(self.tipago)


class Sala(models.Model):
    objects = None
    descripcion = models.CharField(max_length=225)
    asientos = models.CharField(max_length=225)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Sala"
        verbose_name = "sala"
        verbose_name_plural = "salas"
        ordering = ['fecha_creacion', 'descripcion']

    def __str__(self):
        return '{}'.format(self.descripcion)


class Asiento(models.Model):
    objects = None
    codigo = models.CharField(max_length=255)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Asiento"
        verbose_name = "asiento"
        verbose_name_plural = "asientos"
        ordering = ['fecha_creacion', 'codigo']

    def __str__(self):
        return '{}'.format(self.codigo)

class Promocion(models.Model):
    objects = None
    tipopromocion = models.CharField(max_length=225)
    descuento = models.CharField(max_length=225)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Promocion"
        verbose_name = "promocion"
        verbose_name_plural = "promociones"
        ordering = ['fecha_creacion', 'descuento']

    def __str__(self):
        return '{}'.format(self.descuento)


class Ticket(models.Model):
    objects = None
    asiento = ForeignKey(Asiento, on_delete=models.CASCADE, blank=True, null=True)
    sala = ForeignKey(Sala, on_delete=models.CASCADE, blank=True, null=True)
    pomocion = ForeignKey(Promocion, on_delete=models.CASCADE, blank=True, null=True)
    metodopago = ForeignKey(MetodoPago, on_delete=models.CASCADE, blank=True, null=True)
    numticket = models.IntegerField(default=1)
    precio_unitario = ForeignKey(Venta, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Ticket"
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
        ordering = ['fecha_creacion', 'numticket']

    def __str__(self):
        return '{}{}{}{}{}'.format(self.numticket, "", self.sala, "", self.asiento)


class Presentacion(models.Model):
    UNIDAD = 'UN'
    DOSD = '2D'
    TRESD = '3D'
    UNIDAD_CHOICES = [
        (DOSD, 'Dosde'),
        (TRESD, 'Tresde'),
        (UNIDAD, 'Unidad'),
    ]
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    unidad = models.CharField(max_length=2, choices=UNIDAD_CHOICES, default=UNIDAD)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "presentacion"
        verbose_name = "presentacion"
        verbose_name_plural = "presentaciones"
        ordering = ['fecha_creacion', 'ticket']

    def __str__(self):
        return '{}'.format(self.unidad)



class Categoria(models.Model):
    objects = None
    genero = models.CharField(max_length=225)
    tipo = models.CharField(max_length=225)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Categoria"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['fecha_creacion', 'genero']

    def __str__(self):
        return '{}'.format(self.genero)


class Horario(models.Model):
    objects = None
    detalle = models.CharField(max_length=225)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Horario"
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        ordering = ['fecha_creacion', 'detalle']

    def __str__(self):
        return '{}'.format(self.detalle)


class Cartelera(models.Model):
    objects = None
    presentacion = models.CharField(max_length=255)
    peliculas = models.CharField(max_length=255)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Cartelera"
        verbose_name = "Cartelera"
        verbose_name_plural = "Carteleras"
        ordering = ['fecha_creacion', 'presentacion']

    def __str__(self):
        return '{}'.format(self.presentacion)

class Pelicula(models.Model):
    categoria = ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    horario = ForeignKey(Horario, on_delete=models.CASCADE, blank=True, null=True)
    cartelera = ForeignKey(Cartelera, on_delete=models.CASCADE, blank=True, null=True)
    titulo = models.CharField(max_length=225)
    estado = models.IntegerField(default=1)
    objects = None

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Pelicula"
        verbose_name = "pelicula"
        verbose_name_plural = "peliculas"
        ordering = ['fecha_creacion', 'titulo']

    def __str__(self):
        return '{}'.format(self.titulo)


class DetalleVenta(models.Model):
    objects = None
    ticket = ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, blank=True, null=True)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE, blank=True, null=True)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "DetalleVenta"
        verbose_name = "detalleventa"
        verbose_name_plural = "detallesventas"
        ordering = ['fecha_creacion', 'ticket']

    def __str__(self):
        return '{}'.format(self.ticket)


class Vendedor(models.Model):
    objects = None
    detalleventa = ForeignKey(DetalleVenta, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=225)
    apellido = models.CharField(max_length=225)
    dni = models.IntegerField(default=1)
    estado = models.IntegerField(default=1)

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=False, null=False)
    usuario_creacion = models.CharField(max_length=15)
    usuario_modificacion = models.CharField(max_length=15)

    class Meta:
        db_table = "Vendedor"
        verbose_name = "vendedor"
        verbose_name_plural = "vendedores"
        ordering = ['fecha_creacion', 'apellido']

    def __str__(self):
        return '{}{}'.format(self.apellido, self.nombre)

# class CabeceraVenta(models.Model):
#     objects = None
#     fecha_venta = models.DateTimeField()
#     numero_venta = models.CharField(max_length=40)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
#     total_venta = models.DecimalField(max_digits=16, decimal_places=6)
#     estado = models.IntegerField(default=1)
#
#     fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
#     usuario_creacion = models.CharField(max_length=15)
#     usuario_modificacion = models.CharField(max_length=15)
#
#     class Meta:
#         db_table = "cabecera_venta"
#         verbose_name = "venta"
#         verbose_name_plural = "ventas"
#         ordering = ['fecha_venta', 'cliente']
#
#     def __str__(self):
#         return '{}{}'.format(self.cliente, self.numero_venta)
#
#
# class DetalleVnt(models.Model):
#     cabecera_venta = models.ForeignKey(CabeceraVenta, on_delete=models.CASCADE, blank=True, null=True)
#     ticket = ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True, related_name="presentacion")
#     presentacion = ForeignKey(Presentacion, on_delete=models.CASCADE, blank=True, null=True)
#     cantidad_ticket = ForeignKey(Venta, on_delete=models.CASCADE, blank=True, null=True)
#     precio_unitario = ForeignKey(Ticket, on_delete=models.CASCADE, blank=True, null=True)
#     total_venta_ticket = models.IntegerField(default=1)
#     codigo = models.IntegerField(blank=True, null=True)
#
#     estado = models.IntegerField(default=1)
#
#     fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
#     usuario_creacion = models.CharField(max_length=15)
#     usuario_modificacion = models.CharField(max_length=15)
#
#     class Meta:
#         db_table = "detalle_vnt"
#         verbose_name = "detalle vnt"
#         verbose_name_plural = "detalle vnts"
#         ordering = ['ticket']
#
#     def __str__(self):
#         return '{}{}'.format(self.ticket, self.presentacion)



