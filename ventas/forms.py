from django import forms
from django.forms import Form, ModelForm, formset_factory
from ventas.models import Cliente, Venta, Ticket, DetalleVenta, MetodoPago, Vendedor, Sala, Asiento, Promocion, Pelicula,Categoria, Cartelera, Horario
from .models import Presentacion
from django.forms.models import inlineformset_factory

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'billing_address','email']



class BuscarClienteForm(Form):
    nombre= forms.CharField(max_length=200)
    apellido = forms.CharField(max_length=200)
    desde=forms.DateTimeField(label="Desde",required=True,widget=forms.DateInput(format=('%Y-%m-%d'),
                                                       attrs={
                                                           'placeholder': 'Seleccione una fecha',
                                                           'type': 'date',
                                                           'size': 30}))
    hasta = forms.DateTimeField(label="Hasta",required=True,widget=forms.DateInput(format=('%Y-%m-%d'),
                                                       attrs={
                                                           'placeholder': 'Seleccione una fecha',
                                                           'type': 'date',
                                                           'size':30}))


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'cantidad_ticket', 'precio_unitario', 'total_venta_ticket']

class BuscarVentaForm(Form):
    cliente = forms.CharField(max_length=200)
    cantidad_ticket = forms.CharField(max_length=200)
    precio_unitario = forms.CharField(max_length=200)
    total_venta_ticket = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['numticket', 'asiento', 'sala', 'pomocion', 'precio_unitario', 'metodopago']

class BuscarTicketForm(Form):
    numticket = forms.IntegerField(max_value=None)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['ticket', 'presentacion', 'pelicula']

class BuscarDetalleVentaForm(Form):
    ticket = forms.CharField(max_length=200)
    presentacion = forms.CharField(max_length=200)
    pelicula = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ['tipago', 'descripcion']

class BuscarMetodoPagoForm(Form):
    tipago = forms.CharField(max_length=200)
    descripcion = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nombre', 'apellido', 'dni', 'detalleventa']

class BuscarVendedorForm(Form):
    nombre = forms.CharField(max_length=200)
    apellido = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['descripcion', 'asientos']

class BuscarSalaForm(Form):
    descripcion = forms.CharField(max_length=200)
    asientos = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class AsientoForm(forms.ModelForm):
    class Meta:
        model = Asiento
        fields = {'codigo'}

class BuscarAsientoForm(Form):
    codigo = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['tipopromocion', 'descuento']

class BuscarPromocionForm(Form):
    tipopromocion = forms.CharField(max_length=200)
    descuento = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'categoria', 'cartelera', 'horario']

class BuscarPeliculaForm(Form):
    titulo = forms.CharField(max_length=200)
    categoria = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['genero', 'tipo']

class BuscarCategoriaForm(Form):
    genero = forms.CharField(max_length=200)
    tipo = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class CarteleraForm(forms.ModelForm):
    class Meta:
        model = Cartelera
        fields = ['presentacion', 'peliculas']

class BuscarCarteleraForm(Form):
    presentacion = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['detalle']

class BuscarHorarioForm(Form):
    detalle = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))


class PresentacionForm(ModelForm):
    class Meta:
        model = Presentacion
        fields = ['ticket', 'unidad']

class BuscarPresentacionForm(Form):
    ticket = forms.CharField(max_length=200)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'),
                                                                                     attrs={
                                                                                         'placeholder': 'Seleccione una fecha',
                                                                                         'type': 'date',
                                                                                         'size': 30}))



# class CabeceraVentaForm(ModelForm):
#     class Meta:
#         model = CabeceraVenta
#         fields = ['fecha_venta', 'numero_venta', 'cliente', 'total_venta']
#         widgets = {'fecha_venta': forms.DateInput(format=('%Y-%m-%d'),
#                                             attrs={
#                                                 'placeholder': 'Selecione una fecha',
#                                                 'type': 'date',
#                                                 'size': 30})}

# CabeceraFormSet= formset_factory(CabeceraVentaForm)
#
# class DetalleVntForm(ModelForm):
#     class Meta:
#         model = DetalleVnt
#         fields = ['ticket', 'presentacion', 'cantidad_ticket', 'precio_unitario', 'total_venta_ticket']
#         # widgets = {
#         #     'producto': forms.Select(attrs={'id': 'nombre'}),
#         #     'presentacion': forms.Select(attrs={'id': 'unidad'}),
#         # }


# CabeceraFormSet = inlineformset_factory(
#     Cliente,
#     cabeceraVenta,
#     form=CabeceraVentaForm,
#     extra=0, can_delete=True, can_delete_extra=True,
#     min_num=1,
# )

# DetalleFormSet = inlineformset_factory(
#     CabeceraVenta,
#     DetalleVnt,
#     form=DetalleVentaForm,
#     extra=0, can_delete=True, can_delete_extra=True,
#     min_num=1,
# )
# class DetalleVntForm(ModelForm):
#     class Meta:
#         model = DetalleVnt
#         fields = ['codigo', 'ticket', 'presentacion', 'cantidad_ticket', 'precio_unitario', 'total_venta_ticket']
#         widgets = {
#             'ticket': forms.Select(attrs={'id': 'numticket'}),
#             'presentacion': forms.Select(attrs={'id': 'unidad'}),
#         }

class BuscarFacturaForm(Form):
    cliente = forms.CharField(max_length=255)
    numero_venta = forms.CharField(max_length=255)
    desde = forms.DateTimeField(label="Desde", required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
        'placeholder': 'Seleccione una fecha',
        'type': 'date', 'size': 30}))
    hasta = forms.DateTimeField(label="Hasta", required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={
        'placeholder': 'Seleccione una fecha', 'type': 'date', 'size': 30}))
    # btn = forms.CharField(label="", widget=forms.HiddenInput(), required=False)


class PalabraForm(forms.Form):
    palabra = forms.CharField(max_length=255)
