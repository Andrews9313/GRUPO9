from django.shortcuts import render, redirect, get_object_or_404
from ventas.models import Cliente, DetalleVenta, Venta, Ticket, MetodoPago, Vendedor, Sala, Asiento, Promocion, \
    Pelicula, Cartelera, Categoria, Horario, Presentacion
from ventas.forms import ClienteForm, DetalleVentaForm, TicketForm, MetodoPagoForm, VendedorForm, SalaForm, AsientoForm, \
    PromocionForm, PeliculaForm, CategoriaForm, CarteleraForm, HorarioForm, VentaForm, \
    DetalleVentaForm, PresentacionForm
from .forms import BuscarPeliculaForm, BuscarCarteleraForm, BuscarTicketForm, BuscarPromocionForm, BuscarClienteForm, \
    BuscarAsientoForm, BuscarDetalleVentaForm, BuscarVentaForm, \
    BuscarVendedorForm, BuscarHorarioForm, BuscarCategoriaForm, BuscarSalaForm, BuscarMetodoPagoForm, BuscarPresentacionForm
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.forms import inlineformset_factory
import io
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

# def crear_cliente(request):
#     if request.method == "POST":
#         clienteForm = ClienteForm(request.POST or None)
#         if clienteForm.is_valid():
#             clienteForm.save()
#             messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
#             return redirect("consultar_cliente")
#     else:
#         clienteForm = ClienteForm
#     return render(request, "cliente/crear_cliente.html", {"form": clienteForm})

def crear_cliente(request):
    if request.method == "POST":
        clienteForm = ClienteForm(request.POST )
        if clienteForm.is_valid():
            nombre = clienteForm.cleaned_data['nombre']
            apellido = clienteForm.cleaned_data['apellido']
            billing_address = clienteForm.cleaned_data['billing_address']
            email = clienteForm.cleaned_data['email']
            usuario_creacion = request.user
            usuario_modificacion = request.user
            Cliente.objects.create(nombre=nombre, apellido=apellido, billing_address=billing_address,
                                   email=email, usuario_creacion=usuario_creacion,
                                   usuario_modificacion=usuario_modificacion)
            messages.add_message(request, messages.SUCCESS, 'Su resgistro fue un existo')
            return redirect('consultar_cliente')
        else:
            messages.add_message(request, messages.WARNING, "No se registro exitosamente")
            clienteForm = ClienteForm()
    else:
        clienteForm = ClienteForm()
    return render(request, "cliente/crear_cliente.html", {'clienteForm': clienteForm})


def consultar_cliente(request):
    lista_clientes = Cliente.objects.filter(estado=1)
    buscarcliente = BuscarClienteForm()
    return render(request, "cliente/consultar_cliente.html", {"lista_clientes": lista_clientes,
                                                               "buscar_clientes": buscarcliente})

# def consultar_cliente(request):
#     clientes = Cliente.objects.filter(estado=1)
#     buscarCliente = BuscarClienteForm()
#     return render(request, "cliente/consultar_cliente.html",
#                   {"lista_clientes": clientes, 'buscar_cliente': buscarCliente})

# def buscar_cliente(request):
#     global clientes
#     if request.method == "POST":
#         buscarCliente = BuscarClienteForm(request.POST or None)
#         if buscarCliente.is_valid():
#             nombre = buscarCliente.cleaned_data['nombre']
#             apellido = buscarCliente.cleaned_data['apellido']
#             desde = buscarCliente.cleaned_data['desde']
#             hasta = buscarCliente.cleaned_data['hasta']
#             clientes = Cliente.objects.filter(Q(nombre__startswith=nombre) & Q(apellido__startswith=apellido) & Q(fecha_creacion__range=(desde, hasta)))
#     else:
#         buscarCliente = BuscarClienteForm()
#     return render(request, "cliente/consultar_cliente.html",{"lista_cliente": clientes, 'buscar_cliente': buscarCliente})

# def buscar_cliente(request):
#     global lista_clientes
#     if request.method == "POST":
#         buscarcliente = BuscarClienteForm(request.POST or None)
#         if buscarcliente.is_valid():
#             nombre = buscarcliente.cleaned_data["nombre"]
#             apellido = buscarcliente.cleaned_data["apellido"]
#             desde = buscarcliente.cleaned_data["desde"]
#             hasta = buscarcliente.cleaned_data["hasta"]
#             lista_clientes = Cliente.objects.filter(Q(nombre__startswith=nombre) and Q(apellido__startswith=apellido),fecha_creacion__range=(desde,hasta))
#         else:
#             buscarcliente=BuscarClienteForm()
#         return render(request,"cliente/consultar_cliente.html", {"buscar_cliente": buscarcliente, "lista_clientes": lista_clientes})

def buscar_cliente(request):
    global lista_clientes
    if request.method=="POST":
        buscarcliente=BuscarClienteForm(request.POST or None)
        if buscarcliente.is_valid():
            nombre=buscarcliente.cleaned_data["nombre"]
            apellido = buscarcliente.cleaned_data["apellido"]
            desde=buscarcliente.cleaned_data["desde"]
            hasta=buscarcliente.cleaned_data["hasta"]
            lista_clientes=Cliente.objects.filter(Q(nombre__startswith=nombre) and Q(apellido__startswith=apellido), fecha_creacion__range=(desde, hasta))
        else:
            buscarcliente=BuscarClienteForm()
        return render(request,"cliente/consultar_cliente.html", {"buscar_clientes": buscarcliente, "lista_clientes": lista_clientes})

def exportar_lista_cliente(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_cliente.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        clientes = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte de Clientes", styles['Heading1'])
        clientes.append(header)

        buscar_cliente = BuscarClienteForm(request.POST or None)
        if buscar_cliente.is_valid():
            nombre = buscar_cliente.cleaned_data['nombre']
            apellido = buscar_cliente.cleaned_data['apellido']
            desde = buscar_cliente.cleaned_data['desde']
            hasta = buscar_cliente.cleaned_data['hasta']
            lista_clientes = Cliente.objects.filter(Q(nombre__startswith=nombre) and Q(apellido__startswith=apellido),
                                                    fecha_creacion__range=(desde, hasta))

            headings = ('Fecha_creacion', 'nombre','apellido',
                        'billing_address','Email', 'Estado')
            allclientes = [(c.fecha_creacion, c.nombre,c.apellido,c.billing_address,c.email, c.estado)
                           for c in lista_clientes]
            t = Table([headings] + allclientes)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            clientes.append(t)
            doc.build(clientes)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_cliente(request, id):
    if request.method == "POST":
        cliente = get_object_or_404(Cliente, pk=id)
        clienteForm = ClienteForm(request.POST or None, instance=cliente)
        if clienteForm.is_valid():
            clienteForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_cliente')
    else:  # GET
        cliente = get_object_or_404(Cliente, pk=id)
        clienteForm = ClienteForm(instance=cliente)
    return render(request, "cliente/modificar_cliente.html", {'form': clienteForm})

def eliminar_cliente(request, id):
    if request.method == "POST":
        cliente = get_object_or_404(Cliente, pk=id)
        clienteForm = ClienteForm(request.POST or None, instance=cliente)
        if clienteForm.is_valid():
            clienteForm.save(commit=False)
            cliente.estado = 0
            clienteForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_cliente')
    else:  # GET
        cliente = get_object_or_404(Cliente, pk=id)
        clienteForm = ClienteForm(instance=cliente)
    return render(request, "cliente/eliminar_cliente.html", {'form': clienteForm})

# def exportar_lista_cliente(request):
#     # Create a file-like buffer to receive PDF data.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="exportar_lista_cliente.pdf"'
#     if request.method == "POST":
#         buffer = io.BytesIO()
#
#         doc = SimpleDocTemplate(buffer,
#                                 rightMargin=inch / 4,
#                                 leftMargin=inch / 4,
#                                 topMargin=inch / 2,
#                                 bottomMargin=inch / 4,
#                                 pagesize=A4)
#
#         styles = getSampleStyleSheet()
#         styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
#         styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))
#
#         clientes = []
#         styles = getSampleStyleSheet()
#         header = Paragraph("  Reporte De Cliente", styles['Heading1'])
#         clientes.append(header)
#
#         buscarcliente = BuscarClienteForm(request.POST or None)
#         if buscarcliente.is_valid():
#             nombre = buscarcliente.cleaned_data['nombre']
#             apellido = buscarcliente.cleaned_data['apellido']
#             desde = buscarcliente.cleaned_data['desde']
#             hasta = buscarcliente.cleaned_data['hasta']
#             # lista_clientes = Cliente.objects.filter(Q(nombre__startswith=nombre) and Q(apellido__startswith=apellido),
#             #                                         fecha_creacion__range=(desde, hasta))
#             lista_clientes = Cliente.objects.all()
#             headings = ('fecha', 'Nombre', 'Apellido', 'Email', 'Direccion', 'Estado')
#             allclientes = [(p.fecha_creacion, p.nombre, p.apellido, p.email, p.billing_address, p.estado)
#                                  for p in lista_clientes]
#
#             t = Table([headings] + allclientes)
#             t.setStyle(TableStyle(
#                 [
#                     ('GRID', (0, 0), (9, -1), 1, colors.coral),
#                     ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
#                     ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
#                 ]
#             ))
#             clientes.append(t)
#             doc.build(clientes)
#             response.write(buffer.getvalue())
#             buffer.close()
#
#     return response


def crear_detalleventa(request):
    if request.method == "POST":
        detalleventaForm = DetalleVentaForm(request.POST or None)
        if detalleventaForm.is_valid():
           detalleventaForm.save()
           messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
           return redirect("consultar_detalleventa")
    else:  # GET
        detalleventaForm = DetalleVentaForm
    return render(request, "detalleventa/crear_detalleventa.html", {"form": detalleventaForm})


def consultar_detalleventa(request):
    detallesventas = DetalleVenta.objects.filter(estado=1)
    buscarDetalleVenta = BuscarDetalleVentaForm()
    return render(request, "detalleventa/consultar_detalleventa.html", {"lista_detallesventas": detallesventas,
                                                                       'buscar_detallesventas': buscarDetalleVenta})

def buscar_detalleventa(request):
    global buscarDetalleVenta, lista_detallesventas
    if request.method == "POST":
        buscarDetalleVenta = BuscarDetalleVentaForm(request.POST or None)
        if buscarDetalleVenta.is_valid():
            ticket = buscarDetalleVenta.cleaned_data['ticket']
            presentacion = buscarDetalleVenta.cleaned_data['presentacion']
            pelicula = buscarDetalleVenta.cleaned_data['pelicula']
            desde = buscarDetalleVenta.cleaned_data['desde']
            hasta = buscarDetalleVenta.cleaned_data['hasta']
            lista_detallesventas = DetalleVenta.objects.filter(Q(ticket__numticket__startswith=ticket) and Q(presentacion__unidad__startswith=presentacion) and Q(pelicula__titulo__startswith=pelicula), fecha_creacion__range=(desde, hasta))
    return render(request, "detalleventa/consultar_detalleventa.html",{"lista_detallesventas": lista_detallesventas,
                                                                       "buscar_detallesventas": buscarDetalleVenta})

def exportar_lista_detalleventa(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_detalleventa.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        detallesventas = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Detalle Venta", styles['Heading1'])
        detallesventas.append(header)

        buscardetalleventa = BuscarDetalleVentaForm(request.POST or None)
        if buscardetalleventa.is_valid():
            ticket = buscardetalleventa.cleaned_data['ticket']
            presentacion = buscardetalleventa.cleaned_data['presentacion']
            pelicula = buscardetalleventa.cleaned_data['pelicula']
            desde = buscardetalleventa.cleaned_data['desde']
            hasta = buscardetalleventa.cleaned_data['hasta']
            lista_detallesventas = DetalleVenta.objects.filter(Q(ticket__numticket__startswith=ticket) and Q(presentacion__unidad__startswith=presentacion) and Q(pelicula__titulo__startswith=pelicula) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'Ticket', 'Presentacion', 'Pelicula', 'Estado')
            alldetallesventas = [(p.fecha_creacion, p.ticket, p.presentacion, p.pelicula, p.estado)
                                 for p in lista_detallesventas]

            t = Table([headings] + alldetallesventas)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            detallesventas.append(t)
            doc.build(detallesventas)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_detalleventa(request, id):
    if request.method == "POST":
        detalleventa = get_object_or_404(DetalleVenta, pk=id)
        detalleventaForm = DetalleVentaForm(request.POST or None, instance=detalleventa)
        if detalleventaForm.is_valid():
            detalleventaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modifcado Exitosamente")
            return redirect('consultar_detalleventa')
    else:  # GET
        detalleventa = get_object_or_404(DetalleVenta, pk=id)
        detalleventaForm = DetalleVentaForm(instance=detalleventa)
    return render(request, "detalleventa/modificar_detalleventa.html", {'form': detalleventaForm})

def eliminar_detalleventa(request, id):
    if request.method == "POST":
        detalleventa = get_object_or_404(DetalleVenta, pk=id)
        detalleventaForm = DetalleVentaForm(request.POST or None, instance=detalleventa)
        if detalleventaForm.is_valid():
            detalleventaForm.save(commit=False)
            detalleventa.estado = 0
            detalleventaForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_detalleventa')
    else:  # GET
        detalleventa = get_object_or_404(DetalleVenta, pk=id)
        detalleventaForm = DetalleVentaForm(instance=detalleventa)
    return render(request, "detalleventa/eliminar_detalleventa.html", {'form': detalleventaForm})

def crear_venta(request):
    if request.method == "POST":
        ventaForm = VentaForm(request.POST or None)
        if ventaForm.is_valid():
            ventaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_venta")
    else:  # GET
        ventaForm = VentaForm
    return render(request, "venta/crear_venta.html", {"form": ventaForm})


def consultar_venta(request):
    ventas = Venta.objects.filter(estado=1)
    buscarVenta = BuscarVentaForm()
    return render(request, "venta/consultar_venta.html", {"lista_ventas": ventas, 'buscar_ventas': buscarVenta})

def buscar_venta(request):

    if request.method == "POST":
        buscarVenta = BuscarVentaForm(request.POST or None)
        if buscarVenta.is_valid():
            cliente = buscarVenta.cleaned_data['cliente']
            cantidad_ticket = buscarVenta.cleaned_data['cantidad_ticket']
            precio_unitario = buscarVenta.cleaned_data['precio_unitario']
            total_venta_ticket = buscarVenta.cleaned_data['total_venta_ticket']
            desde = buscarVenta.cleaned_data['desde']
            hasta = buscarVenta.cleaned_data['hasta']
            lista_ventas = Venta.objects.filter(Q(cliente__nombre__contains=cliente) and Q(cantidad_ticket__iexact=cantidad_ticket) and Q(precio_unitario__iexact=precio_unitario) and Q(total_venta_ticket__iexact=total_venta_ticket) and Q(fecha_creacion__range=(desde, hasta)))
    return render(request, "venta/consultar_venta.html", {"lista_ventas": lista_ventas, 'buscar_ventas': buscarVenta})

def exportar_lista_venta(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_venta.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        ventas = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Venta", styles['Heading1'])
        ventas.append(header)

        buscarventa = BuscarVentaForm(request.POST or None)
        if buscarventa.is_valid():
            cliente = buscarventa.cleaned_data['cliente']
            precio_unitario = buscarventa.cleaned_data['precio_unitario']
            cantidad_ticket = buscarventa.cleaned_data['cantidad_ticket']
            total_venta_ticket = buscarventa.cleaned_data['total_venta_ticket']
            desde = buscarventa.cleaned_data['desde']
            hasta = buscarventa.cleaned_data['hasta']
            lista_ventas = Venta.objects.filter(Q(cliente__nombre__contains=cliente) and Q(cantidad_ticket__iexact=cantidad_ticket) and Q(precio_unitario__iexact=precio_unitario) and Q(total_venta_ticket__iexact=total_venta_ticket) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('Fecha', 'Cliente', 'Cantida_Ticket', 'Precio_Unitario', 'Total_Venta_Ticket', 'Estado')
            allventas = [(p.fecha_creacion, p.cliente, p.cantidad_ticket, p.precio_unitario, p.total_venta_ticket, p.estado)
                                 for p in lista_ventas]

            t = Table([headings] + allventas)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            ventas.append(t)
            doc.build(ventas)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_venta(request, id):
    if request.method == "POST":
        venta = get_object_or_404(Venta, pk=id)
        ventaForm = VentaForm(request.POST or None, instance=venta)
        if ventaForm.is_valid():
            ventaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modifcado Exitosamente")
            return redirect('consultar_venta')
    else:  # GET
        venta = get_object_or_404(Venta, pk=id)
        ventaForm = VentaForm(instance=venta)
    return render(request, "venta/modificar_venta.html", {'form': ventaForm})

def eliminar_venta(request, id):
    if request.method == "POST":
        venta = get_object_or_404(Venta, pk=id)
        ventaForm = VentaForm(request.POST or None, instance=venta)
        if ventaForm.is_valid():
            ventaForm.save(commit=False)
            venta.estado = 0
            ventaForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_venta')
    else:  # GET
        venta = get_object_or_404(Venta, pk=id)
        ventaForm = VentaForm(instance=venta)
    return render(request, "venta/eliminar_venta.html", {'form': ventaForm})

def crear_ticket(request):
    if request.method == "POST":
        ticketForm = TicketForm(request.POST or None)
        if ticketForm.is_valid():
            ticketForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_ticket")
    else:  # GET
        ticketForm = TicketForm
    return render(request, "ticket/crear_ticket.html", {"form": ticketForm})


def consultar_ticket(request):
    lista_tickets = Ticket.objects.filter(estado=1)
    buscarTicket = BuscarTicketForm()
    return render(request, "ticket/consultar_ticket.html", {"lista_tickets": lista_tickets,
                                                            "buscar_tickets": buscarTicket})

def buscar_ticket(request):
    global lista_tickets
    if request.method == "POST":
        buscarTicket = BuscarTicketForm(request.POST or None)
        if buscarTicket.is_valid():
            numticket = buscarTicket.cleaned_data['numticket']
            desde = buscarTicket.cleaned_data['desde']
            hasta = buscarTicket.cleaned_data['hasta']
            lista_tickets = Ticket.objects.filter(Q(numticket__exact=numticket) & Q(fecha_creacion__range=(desde, hasta)))
        else:
            buscarTicket = BuscarTicketForm()
        return render(request, "ticket/consultar_ticket.html", {'buscar_tickets': buscarTicket,
                                                                "lista_tickets": lista_tickets})

# def lista_tickets(request):
#     tickets = Ticket.objects.filter(estado=1)
#     return render(request, "ticket/lista_tickets.html", {"lista_tickets": tickets})

def exportar_lista_ticket(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_ticket.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        tickets = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Ticket", styles['Heading1'])
        tickets.append(header)

        buscarticket = BuscarTicketForm(request.POST or None)
        if buscarticket.is_valid():
            numticket = buscarticket.cleaned_data['numticket']
            desde = buscarticket.cleaned_data['desde']
            hasta = buscarticket.cleaned_data['hasta']
            lista_tickets = Ticket.objects.filter(Q(numticket__exact=numticket) & Q(fecha_creacion__range=(desde, hasta)))
            headings = ('Fecha', 'Asiento', 'Sala', 'Pomocion', 'Metodo Pago', 'Numticket', 'Precio Unitario', 'Estado')
            alltickets = [(p.fecha_creacion, p.asiento, p.sala, p.pomocion, p.metodopago, p.numticket, p.precio_unitario, p.estado)
                                 for p in lista_tickets]

            t = Table([headings] + alltickets)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            tickets.append(t)
            doc.build(tickets)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_ticket(request, id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, pk=id)
        ticketForm = TicketForm(request.POST or None, instance=ticket)
        if ticketForm.is_valid():
            ticketForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_ticket')
    else:  # GET
        ticket = get_object_or_404(Ticket, pk=id)
        ticketForm = TicketForm(instance=ticket)
    return render(request, "ticket/modificar_ticket.html", {'form': ticketForm})

def eliminar_ticket(request, id):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, pk=id)
        ticketForm = TicketForm(request.POST or None, instance=ticket)
        if ticketForm.is_valid():
            ticketForm.save(commit=False)
            ticket.estado = 0
            ticketForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_ticket')
    else:  # GET
        ticket = get_object_or_404(Ticket, pk=id)
        ticketForm = TicketForm(instance=ticket)
    return render(request, "ticket/eliminar_ticket.html", {'form': ticketForm})

def crear_metodopago(request):
    if request.method == "POST":
        metodopagoForm = MetodoPagoForm(request.POST or None)
        if metodopagoForm.is_valid():
            metodopagoForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_metodopago")
    else:  # GET
        metodopagoForm = MetodoPagoForm
    return render(request, "metodopago/crear_metodopago.html", {"form": metodopagoForm})


def consultar_metodopago(request):
    metodospagos = MetodoPago.objects.filter(estado=1)
    buscarMetodoPago = BuscarMetodoPagoForm()
    return render(request, "metodopago/consultar_metodopago.html",
                  {"lista_metodospagos": metodospagos, 'buscar_metodospagos': buscarMetodoPago})

def buscar_metodopago(request):
    global metodospagos, buscarMetodoPago
    if request.method == "POST":
        buscarMetodoPago = BuscarMetodoPagoForm(request.POST or None)
        if buscarMetodoPago.is_valid():
            tipago = buscarMetodoPago.cleaned_data['tipago']
            descripcion = buscarMetodoPago.cleaned_data['descripcion']
            desde = buscarMetodoPago.cleaned_data['desde']
            hasta = buscarMetodoPago.cleaned_data['hasta']
            lista_metodospagos = MetodoPago.objects.filter(Q(tipago__iexact=tipago) and Q(descripcion__iexact=descripcion) and Q(fecha_creacion__range=(desde, hasta)))
    return render(request, "metodopago/consultar_metodopago.html",
                  {"lista_metodospagos": lista_metodospagos, 'buscar_metodospagos': buscarMetodoPago})

def exportar_lista_metodopago(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_metodopago.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        metodospagos = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Metodo Pago", styles['Heading1'])
        metodospagos.append(header)

        buscarmetodopago = BuscarMetodoPagoForm(request.POST or None)
        if buscarmetodopago.is_valid():
            tipago = buscarmetodopago.cleaned_data['tipago']
            descripcion = buscarmetodopago.cleaned_data['descripcion']
            desde = buscarmetodopago.cleaned_data['desde']
            hasta = buscarmetodopago.cleaned_data['hasta']
            lista_metodospagos = MetodoPago.objects.filter(Q(tipago__iexact=tipago) and Q(descripcion__iexact=descripcion) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha','tipago ', 'Descripcion', 'Estado')
            allmetodospagos = [(p.fecha_creacion, p.tipago , p.descripcion, p.estado)
                                 for p in lista_metodospagos]

            t = Table([headings] + allmetodospagos)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            metodospagos.append(t)
            doc.build(metodospagos)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_metodopago(request, id):
    if request.method == "POST":
        metodopago = get_object_or_404(MetodoPago, pk=id)
        metodopagoForm = MetodoPagoForm(request.POST or None, instance=metodopago)
        if metodopagoForm.is_valid():
            metodopagoForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_metodopago')
    else:  # GET
        metodopago = get_object_or_404(MetodoPago, pk=id)
        metodopagoForm = MetodoPagoForm(instance=metodopago)
    return render(request, "metodopago/modificar_metodopago.html", {'form': metodopagoForm})

def eliminar_metodopago(request, id):
    if request.method == "POST":
        metodopago = get_object_or_404(MetodoPago, pk=id)
        metodopagoForm = MetodoPagoForm(request.POST or None, instance=metodopago)
        if metodopagoForm.is_valid():
            metodopagoForm.save(commit=False)
            metodopago.estado = 0
            metodopagoForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_metodopago')
    else:  # GET
        metodopago = get_object_or_404(MetodoPago, pk=id)
        metodopagoForm = MetodoPagoForm(instance=metodopago)
    return render(request, "metodopago/eliminar_metodopago.html", {'form': metodopagoForm})


def crear_vendedor(request):
    if request.method == "POST":
        vendedorForm = VendedorForm(request.POST or None)
        if vendedorForm.is_valid():
            vendedorForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_vendedor")
    else:  # GET
        vendedorForm = VendedorForm
    return render(request, "vendedor/crear_vendedor.html", {"form": vendedorForm})


def consultar_vendedor(request):
    vendedores = Vendedor.objects.filter(estado=1)
    buscarVendedor = BuscarVendedorForm()
    return render(request, "vendedor/consultar_vendedor.html",
                  {"lista_vendedores": vendedores, 'buscar_vendedor': buscarVendedor})

def buscar_vendedor(request):
    global vendedores
    if request.method == "POST":
        buscarVendedor = BuscarVendedorForm(request.POST or None)
        if buscarVendedor.is_valid():
            nombre = buscarVendedor.cleaned_data['nombre']
            apellido = buscarVendedor.cleaned_data['apellido']
            desde = buscarVendedor.cleaned_data['desde']
            hasta = buscarVendedor.cleaned_data['hasta']
            lista_vendedores = Vendedor.objects.filter(Q(nombre__iexact=nombre) & Q(apellido__iexact=apellido) & Q(fecha_creacion__range=(desde, hasta)))
    else:
        buscarVendedor = BuscarVendedorForm()
    return render(request, "vendedor/consultar_vendedor.html",
                  {"lista_vendedores": lista_vendedores, 'buscar_vendedor': buscarVendedor})

def exportar_lista_vendedor(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_vendedor.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        vendedores = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Vendedor", styles['Heading1'])
        vendedores.append(header)

        buscarvendedor = BuscarVendedorForm(request.POST or None)
        if buscarvendedor.is_valid():
            nombre = buscarvendedor.cleaned_data['nombre']
            apellido = buscarvendedor.cleaned_data['apellido']
            desde = buscarvendedor.cleaned_data['desde']
            hasta = buscarvendedor.cleaned_data['hasta']
            lista_vendedores = Vendedor.objects.filter(Q(nombre__iexact=nombre) & Q(apellido__iexact=apellido) & Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'nombre ', 'apellido', 'dni', 'Estado')
            allvendedores = [(p.fecha_creacion, p.nombre , p.apellido, p.dni, p.estado)
                                 for p in lista_vendedores]

            t = Table([headings] + allvendedores)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            vendedores.append(t)
            doc.build(vendedores)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_vendedor(request, id):
    if request.method == "POST":
        vendedor = get_object_or_404(Vendedor, pk=id)
        vendedorForm = VendedorForm(request.POST or None, instance=vendedor)
        if vendedorForm.is_valid():
            vendedorForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_vendedor')
    else:  # GET
        vendedor = get_object_or_404(Vendedor, pk=id)
        vendedorForm = VendedorForm(instance=vendedor)
    return render(request, "vendedor/modificar_vendedor.html", {'form': vendedorForm})

def eliminar_vendedor(request, id):
    if request.method == "POST":
        vendedor = get_object_or_404(Vendedor, pk=id)
        vendedorForm = VendedorForm(request.POST or None, instance=vendedor)
        if vendedorForm.is_valid():
            vendedorForm.save(commit=False)
            vendedor.estado = 0
            vendedorForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_vendedor')
    else:  # GET
        vendedor = get_object_or_404(Vendedor, pk=id)
        vendedorForm = VendedorForm(instance=vendedor)
    return render(request, "vendedor/eliminar_vendedor.html", {'form': vendedorForm})

def crear_sala(request):
    if request.method == "POST":
        salaForm = SalaForm(request.POST or None)
        if salaForm.is_valid():
            salaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_sala")
    else:  # GET
        salaForm = SalaForm
    return render(request, "sala/crear_sala.html", {"form": salaForm})


def consultar_sala(request):
    salas = Sala.objects.filter(estado=1)
    buscarSala = BuscarSalaForm()
    return render(request, "sala/consultar_sala.html", {"lista_salas": salas, 'buscar_salas': buscarSala})

def buscar_sala(request):
    global  lista_salas
    if request.method == "POST":
        buscarSala = BuscarSalaForm(request.POST or None)
        if buscarSala.is_valid():
            descripcion = buscarSala.cleaned_data['descripcion']
            asientos = buscarSala.cleaned_data['asientos']
            desde = buscarSala.cleaned_data['desde']
            hasta = buscarSala.cleaned_data['hasta']
            lista_salas = Sala.objects.filter(Q(descripcion__iexact=descripcion) and Q(asientos__iexact=asientos) and Q(fecha_creacion__range=(desde, hasta)))
    else:
        buscarSala = BuscarSalaForm()
    return render(request, "sala/consultar_sala.html", {"lista_salas": lista_salas, 'buscar_salas': buscarSala})

def exportar_lista_sala(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_sala.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        salas = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Sala", styles['Heading1'])
        salas.append(header)

        buscarsala = BuscarSalaForm(request.POST or None)
        if buscarsala.is_valid():
            descripcion = buscarsala.cleaned_data['descripcion']
            asientos = buscarsala.cleaned_data['asientos']
            desde = buscarsala.cleaned_data['desde']
            hasta = buscarsala.cleaned_data['hasta']
            lista_salas = Sala.objects.filter(Q(descripcion__iexact=descripcion) and Q(asientos__iexact=asientos) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'descripcion ', 'asientos', 'Estado')
            allsalas = [(p.fecha_creacion, p.descripcion, p.asientos, p.estado)
                                 for p in lista_salas]

            t = Table([headings] + allsalas)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            salas.append(t)
            doc.build(salas)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_sala(request, id):
    if request.method == "POST":
        sala = get_object_or_404(Sala, pk=id)
        salaForm = SalaForm(request.POST or None, instance=sala)
        if salaForm.is_valid():
            salaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_sala')
    else:  # GET
        sala = get_object_or_404(Sala, pk=id)
        salaForm = SalaForm(instance=sala)
    return render(request, "sala/modificar_sala.html", {'form': salaForm})

def eliminar_sala(request, id):
    if request.method == "POST":
        sala = get_object_or_404(Sala, pk=id)
        salaForm = SalaForm(request.POST or None, instance=sala)
        if salaForm.is_valid():
            salaForm.save(commit=False)
            sala.estado = 0
            salaForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_sala')
    else:  # GET
        sala = get_object_or_404(Sala, pk=id)
        salaForm = SalaForm(instance=sala)
    return render(request, "sala/eliminar_sala.html", {'form': salaForm})

def crear_asiento(request):
    if request.method == "POST":
        asientoForm = AsientoForm(request.POST or None)
        if asientoForm.is_valid():
            asientoForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_asiento")
    else:  # GET
        asientoForm = AsientoForm
    return render(request, "asiento/crear_asiento.html", {"form": asientoForm})

def consultar_asiento(request):
    asientos = Asiento.objects.filter(estado=1)
    buscarAsiento = BuscarAsientoForm()
    return render(request, "asiento/consultar_asiento.html",
                  {"lista_asientos": asientos, 'buscar_asientos': buscarAsiento})

def buscar_asiento(request):
    global lista_asientos, buscarAsiento
    if request.method == "POST":
        buscarAsiento = BuscarAsientoForm(request.POST or None)
        if buscarAsiento.is_valid():
            codigo = buscarAsiento.cleaned_data['codigo']
            desde = buscarAsiento.cleaned_data['desde']
            hasta = buscarAsiento.cleaned_data['hasta']
            lista_asientos = Asiento.objects.filter(Q(codigo__iexact=codigo) & Q(fecha_creacion__range=(desde, hasta)))
    return render(request, "asiento/consultar_asiento.html",
                  {"lista_asientos": lista_asientos, 'buscar_asientos': buscarAsiento})

def exportar_lista_asiento(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_asiento.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        asientos = []
        styles = getSampleStyleSheet()
        header = Paragraph("  Reporte De Asiento", styles['Heading1'])
        asientos.append(header)

        buscarasiento = BuscarAsientoForm(request.POST or None)
        if buscarasiento.is_valid():
            codigo = buscarasiento.cleaned_data['codigo']
            desde = buscarasiento.cleaned_data['desde']
            hasta = buscarasiento.cleaned_data['hasta']
            lista_asientos = Asiento.objects.filter(Q(codigo__iexact=codigo) & Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'codigo',  'Estado')
            allasientos = [(p.fecha_creacion, p.codigo,  p.estado)
                                 for p in lista_asientos]

            t = Table([headings] + allasientos)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            asientos.append(t)
            doc.build(asientos)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_asiento(request, id):
    if request.method == "POST":
        asiento = get_object_or_404(Asiento, pk=id)
        asientoForm = AsientoForm(request.POST or None, instance=asiento)
        if asientoForm.is_valid():
            asientoForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_asiento')
    else:  # GET
        asiento = get_object_or_404(Asiento, pk=id)
        asientoForm = AsientoForm(instance=asiento)
    return render(request, "asiento/modificar_asiento.html", {'form': asientoForm})

def eliminar_asiento(request, id):
    if request.method == "POST":
        asiento = get_object_or_404(Asiento, pk=id)
        asientoForm = AsientoForm(request.POST or None, instance=asiento)
        if asientoForm.is_valid():
            asientoForm.save(commit=False)
            asiento.estado = 0
            asientoForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_asiento')
    else:  # GET
        asiento = get_object_or_404(Asiento, pk=id)
        asientoForm = AsientoForm(instance=asiento)
    return render(request, "asiento/eliminar_asiento.html", {'form': asientoForm})


def crear_promocion(request):
    if request.method == "POST":
        promocionForm = PromocionForm(request.POST or None)
        if promocionForm.is_valid():
            promocionForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_promocion")
    else:  # GET
        promocionForm = PromocionForm
    return render(request, "promocion/crear_promocion.html", {"form": promocionForm})


def consultar_promocion(request):
    promociones = Promocion.objects.filter(estado=1)
    buscarPromocion = BuscarPromocionForm()
    return render(request, "Promocion/consultar_promocion.html",
                  {"lista_promociones": promociones, 'buscar_promocion': buscarPromocion})

def buscar_promocion(request):
    global lista_promociones
    if request.method == "POST":
        buscarPromocion = BuscarPromocionForm(request.POST or None)
        if buscarPromocion.is_valid():
            tipopromocion = buscarPromocion.cleaned_data['tipopromocion']
            descuento = buscarPromocion.cleaned_data['descuento']
            desde = buscarPromocion.cleaned_data['desde']
            hasta = buscarPromocion.cleaned_data['hasta']
            lista_promociones = Promocion.objects.filter(
                Q(tipopromocion__iexact=tipopromocion) and Q(descuento__iexact=descuento) and Q(fecha_creacion__range=(desde, hasta)))
    else:
        buscarPromocion = BuscarPromocionForm()
    return render(request, "promocion/consultar_promocion.html",
                  {"lista_promociones": lista_promociones, 'buscar_promocion': buscarPromocion})

def exportar_lista_promocion(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_promocion.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        promociones = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte De Promocion", styles['Heading1'])
        promociones.append(header)

        buscarpromocion = BuscarPromocionForm(request.POST or None)
        if buscarpromocion.is_valid():
            tipopromocion = buscarpromocion.cleaned_data['tipopromocion']
            descuento = buscarpromocion.cleaned_data['descuento']
            desde = buscarpromocion.cleaned_data['desde']
            hasta = buscarpromocion.cleaned_data['hasta']
            lista_promociones = Promocion.objects.filter(
                Q(tipopromocion__iexact=tipopromocion) and Q(descuento__iexact=descuento) and Q(
                    fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'tipopromocion', 'descuento', 'Estado')
            allpromociones = [(p.fecha_creacion, p.tipopromocion, p.descuento, p.estado)
                                 for p in lista_promociones]

            t = Table([headings] + allpromociones)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            promociones.append(t)
            doc.build(promociones)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_promocion(request, id):
    if request.method == "POST":
        promocion = get_object_or_404(Promocion, pk=id)
        promocionForm = PromocionForm(request.POST or None, instance=promocion)
        if promocionForm.is_valid():
            promocionForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_promocion')
    else:  # GET
        promocion = get_object_or_404(Promocion, pk=id)
        promocionForm = PromocionForm(instance=promocion)
    return render(request, "promocion/modificar_promocion.html", {'form': promocionForm})

def eliminar_promocion(request, id):
    if request.method == "POST":
        promocion = get_object_or_404(Promocion, pk=id)
        promocionForm = PromocionForm(request.POST or None, instance=promocion)
        if promocionForm.is_valid():
            promocionForm.save(commit=False)
            promocion.estado = 0
            promocionForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_promocion')
    else:  # GET
        promocion = get_object_or_404(Promocion, pk=id)
        promocionForm = PromocionForm(instance=promocion)
    return render(request, "promocion/eliminar_promocion.html", {'form': promocionForm})


def crear_pelicula(request):
    if request.method == "POST":
        peliculaForm = PeliculaForm(request.POST or None)
        if peliculaForm.is_valid():
            peliculaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_pelicula")
    else:  # GET
        peliculaForm = PeliculaForm
    return render(request, "pelicula/crear_pelicula.html", {"form": peliculaForm})


def consultar_pelicula(request):
    peliculas = Pelicula.objects.filter(estado=1)
    buscarPelicula = BuscarPeliculaForm()
    return render(request, "pelicula/consultar_pelicula.html",
                  {"lista_peliculas": peliculas, 'buscar_peliculas': buscarPelicula})

def buscar_pelicula(request):
    global lista_peliculas
    if request.method == "POST":
        buscarPelicula = BuscarPeliculaForm(request.POST or None)
        if buscarPelicula.is_valid():
            titulo = buscarPelicula.cleaned_data['titulo']
            categoria = buscarPelicula.cleaned_data['categoria']
            desde = buscarPelicula.cleaned_data['desde']
            hasta = buscarPelicula.cleaned_data['hasta']
            lista_peliculas = Pelicula.objects.filter(Q(titulo__iexact=titulo) and Q(categoria__genero__contains=categoria) and Q(fecha_creacion__range=(desde, hasta)))
    else:
        buscarPelicula = BuscarPeliculaForm()
    return render(request, "pelicula/consultar_pelicula.html",
                  {"lista_peliculas": lista_peliculas, 'buscar_peliculas': buscarPelicula})

def exportar_lista_pelicula(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_pelicula.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        peliculas = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte De Pelicula", styles['Heading1'])
        peliculas.append(header)

        buscarpelicula = BuscarPeliculaForm(request.POST or None)
        if buscarpelicula.is_valid():
            titulo = buscarpelicula.cleaned_data['titulo']
            categoria = buscarpelicula.cleaned_data['categoria']
            desde = buscarpelicula.cleaned_data['desde']
            hasta = buscarpelicula.cleaned_data['hasta']
            lista_peliculas = Pelicula.objects.filter(
                Q(titulo__iexact=titulo) and Q(categoria__genero__contains=categoria) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'Titulo', 'Categoria', 'Cartelera', 'Horario', 'Estado')
            allpeliculas = [(p.fecha_creacion, p.titulo, p.categoria, p.cartelera, p.horario,  p.estado)
                                 for p in lista_peliculas]

            t = Table([headings] + allpeliculas)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            peliculas.append(t)
            doc.build(peliculas)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_pelicula(request, id):
    if request.method == "POST":
        pelicula = get_object_or_404(Pelicula, pk=id)
        peliculaForm = PeliculaForm(request.POST or None, instance=pelicula)
        if peliculaForm.is_valid():
            peliculaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_pelicula')
    else:  # GET
        pelicula = get_object_or_404(Pelicula, pk=id)
        peliculaForm = PeliculaForm(instance=pelicula)
    return render(request, "pelicula/modificar_pelicula.html", {'form': peliculaForm})

def eliminar_pelicula(request, id):
    if request.method == "POST":
        pelicula = get_object_or_404(Pelicula, pk=id)
        peliculaForm = PeliculaForm(request.POST or None, instance=pelicula)
        if peliculaForm.is_valid():
            peliculaForm.save(commit=False)
            pelicula.estado = 0
            peliculaForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_pelicula')
    else:  # GET
        pelicula = get_object_or_404(Pelicula, pk=id)
        peliculaForm = PeliculaForm(instance=pelicula)
    return render(request, "pelicula/eliminar_pelicula.html", {'form': peliculaForm})

def crear_categoria(request):
    if request.method == "POST":
        categoriaForm = CategoriaForm(request.POST or None)
        if categoriaForm.is_valid():
            categoriaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_categoria")
    else:  # GET
        categoriaForm = CategoriaForm
    return render(request, "categoria/crear_categoria.html", {"form": categoriaForm})


def consultar_categoria(request):
    categorias = Categoria.objects.filter(estado=1)
    buscarCategoria = BuscarCategoriaForm()
    return render(request, "Categoria/consultar_categoria.html",
                  {"lista_categorias": categorias, 'buscar_categorias': buscarCategoria})

def buscar_categoria(request):
    global lista_categorias
    if request.method == "POST":
        buscarCategoria = BuscarCategoriaForm(request.POST or None)
        if buscarCategoria.is_valid():
            genero = buscarCategoria.cleaned_data['genero']
            tipo = buscarCategoria.cleaned_data['tipo']
            desde = buscarCategoria.cleaned_data['desde']
            hasta = buscarCategoria.cleaned_data['hasta']
            lista_categorias = Categoria.objects.filter(
                Q(genero__iexact=genero) and Q(tipo__iexact=tipo) and Q(fecha_creacion__range=(desde, hasta)))
    else:
        buscarCategoria = BuscarCategoriaForm()
    return render(request, "categoria/consultar_categoria.html",
                  {"lista_categorias": lista_categorias, 'buscar_categorias': buscarCategoria})

def exportar_lista_categoria(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_categoria.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        categorias = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte De Categoria", styles['Heading1'])
        categorias.append(header)

        buscarcategoria = BuscarCategoriaForm(request.POST or None)
        if buscarcategoria.is_valid():
            genero = buscarcategoria.cleaned_data['genero']
            tipo = buscarcategoria.cleaned_data['tipo']
            desde = buscarcategoria.cleaned_data['desde']
            hasta = buscarcategoria.cleaned_data['hasta']
            lista_categorias = Categoria.objects.filter(
                Q(genero__iexact=genero) and Q(tipo__iexact=tipo) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'Genero', 'Tipo', 'Estado')
            allcategorias = [(p.fecha_creacion, p.genero, p.tipo, p.estado)
                                 for p in lista_categorias]

            t = Table([headings] + allcategorias)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            categorias.append(t)
            doc.build(categorias)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_categoria(request, id):
    if request.method == "POST":
        categoria = get_object_or_404(Categoria, pk=id)
        categoriaForm = CategoriaForm(request.POST or None, instance=categoria)
        if categoriaForm.is_valid():
            categoriaForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_categoria')
    else:  # GET
        categoria = get_object_or_404(Categoria, pk=id)
        categoriaForm = CategoriaForm(instance=categoria)
    return render(request, "categoria/modificar_categoria.html", {'form': categoriaForm})

def eliminar_categoria(request, id):
    if request.method == "POST":
        categoria = get_object_or_404(Categoria, pk=id)
        categoriaForm = CategoriaForm(request.POST or None, instance=categoria)
        if categoriaForm.is_valid():
            categoriaForm.save(commit=False)
            categoria.estado = 0
            categoriaForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_categoria')
    else:  # GET
        categoria = get_object_or_404(Categoria, pk=id)
        categoriaForm = CategoriaForm(instance=categoria)
    return render(request, "categoria/eliminar_categoria.html", {'form': categoriaForm})


def crear_cartelera(request):
    if request.method == "POST":
        carteleraForm = CarteleraForm(request.POST or None)
        if carteleraForm.is_valid():
            carteleraForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_cartelera")
    else:  # GET
        carteleraForm = CarteleraForm
    return render(request, "cartelera/crear_cartelera.html", {"form": carteleraForm})


def consultar_cartelera(request):
    carteleras = Cartelera.objects.filter(estado=1)
    buscarCartelera = BuscarCarteleraForm()
    return render(request, "cartelera/consultar_cartelera.html",
                  {"lista_carteleras": carteleras, 'buscar_carteleras': buscarCartelera})

def buscar_cartelera(request):
    global lista_carteleras
    if request.method == "POST":
        buscarCartelera = BuscarCarteleraForm(request.POST or None)
        if buscarCartelera.is_valid():
            presentacion = buscarCartelera.cleaned_data['presentacion']
            desde = buscarCartelera.cleaned_data['desde']
            hasta = buscarCartelera.cleaned_data['hasta']
            lista_carteleras = Cartelera.objects.filter(
                Q(presentacion__iexact=presentacion) and Q(fecha_creacion__range=(desde, hasta)))
    else:
        buscarCartelera = BuscarCarteleraForm()
    return render(request, "cartelera/consultar_cartelera.html",
                  {"lista_carteleras": lista_carteleras, 'buscar_carteleras': buscarCartelera})

def exportar_lista_cartelera(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_cartelera.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        carteleras = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte De Cartelera", styles['Heading1'])
        carteleras.append(header)

        buscarcartelera = BuscarCarteleraForm(request.POST or None)
        if buscarcartelera.is_valid():
            presentacion = buscarcartelera.cleaned_data['presentacion']
            desde = buscarcartelera.cleaned_data['desde']
            hasta = buscarcartelera.cleaned_data['hasta']
            lista_carteleras = Cartelera.objects.filter(
                Q(presentacion__iexact=presentacion) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'Presentacion', 'Peliculas', 'Estado')
            allcarteleras = [(p.fecha_creacion, p.presentacion, p.peliculas, p.estado)
                                 for p in lista_carteleras]

            t = Table([headings] + allcarteleras)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            carteleras.append(t)
            doc.build(carteleras)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_cartelera(request, id):
    if request.method == "POST":
        cartelera = get_object_or_404(Cartelera, pk=id)
        carteleraForm = CarteleraForm(request.POST or None, instance=cartelera)
        if carteleraForm.is_valid():
            carteleraForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_cartelera')
    else:  # GET
        cartelera = get_object_or_404(Cartelera, pk=id)
        carteleraForm = CarteleraForm(instance=cartelera)
    return render(request, "cartelera/modificar_cartelera.html", {'form': carteleraForm})

def eliminar_cartelera(request, id):
    if request.method == "POST":
        cartelera = get_object_or_404(Cartelera, pk=id)
        carteleraForm = CarteleraForm(request.POST or None, instance=cartelera)
        if carteleraForm.is_valid():
            carteleraForm.save(commit=False)
            cartelera.estado = 0
            carteleraForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_cartelera')
    else:  # GET
        cartelera = get_object_or_404(Cartelera, pk=id)
        carteleraForm = CarteleraForm(instance=cartelera)
    return render(request, "cartelera/eliminar_cartelera.html", {'form': carteleraForm})

def crear_horario(request):
    if request.method == "POST":
        horarioForm = HorarioForm(request.POST or None)
        if horarioForm.is_valid():
            horarioForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_horario")
    else:  # GET
        horarioForm = HorarioForm
    return render(request, "horario/crear_horario.html", {"form": horarioForm})


def consultar_horario(request):
    horarios = Horario.objects.filter(estado=1)
    buscarHorario = BuscarHorarioForm()
    return render(request, "horario/consultar_horario.html",
                  {"lista_horarios": horarios, 'buscar_horarios': buscarHorario})

def buscar_horario(request):
    global lista_horarios, buscarHorario
    if request.method == "POST":
        buscarHorario = BuscarHorarioForm(request.POST or None)
        if buscarHorario.is_valid():
            detalle = buscarHorario.cleaned_data['detalle']
            desde = buscarHorario.cleaned_data['desde']
            hasta = buscarHorario.cleaned_data['hasta']
            lista_horarios = Horario.objects.filter(Q(detalle__iexact=detalle) and Q(fecha_creacion__range=(desde, hasta)))
    return render(request, "horario/consultar_horario.html",
                  {"lista_horarios": lista_horarios, 'buscar_horarios': buscarHorario})

def exportar_lista_horario(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_horario.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        horarios = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte De Horario", styles['Heading1'])
        horarios.append(header)

        buscarhorario = BuscarHorarioForm(request.POST or None)
        if buscarhorario.is_valid():
            detalle = buscarhorario.cleaned_data['detalle']
            desde = buscarhorario.cleaned_data['desde']
            hasta = buscarhorario.cleaned_data['hasta']
            lista_horarios = Horario.objects.filter(Q(detalle__iexact=detalle) and Q(fecha_creacion__range=(desde, hasta)))
            headings = ('fecha', 'Detalle', 'Estado')
            allhorarios = [(p.fecha_creacion, p.detalle, p.estado)
                                 for p in lista_horarios]

            t = Table([headings] + allhorarios)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            horarios.append(t)
            doc.build(horarios)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_horario(request, id):
    if request.method == "POST":
        horario = get_object_or_404(Horario, pk=id)
        horarioForm = HorarioForm(request.POST or None, instance=horario)
        if horarioForm.is_valid():
            horarioForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_horario')
    else:  # GET
        horario = get_object_or_404(Horario, pk=id)
        horarioForm = HorarioForm(instance=horario)
    return render(request, "horario/modificar_horario.html", {'form': horarioForm})

def eliminar_horario(request, id):
    if request.method == "POST":
        horario = get_object_or_404(Horario, pk=id)
        horarioForm = HorarioForm(request.POST or None, instance=horario)
        if horarioForm.is_valid():
            horarioForm.save(commit=False)
            horario.estado = 0
            horarioForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_horario')
    else:  # GET
        horario = get_object_or_404(Horario, pk=id)
        horarioForm = HorarioForm(instance=horario)
    return render(request, "horario/eliminar_horario.html", {'form': horarioForm})

def crear_presentacion(request):
    if request.method == "POST":
        presentacionForm = PresentacionForm(request.POST or None)
        if presentacionForm.is_valid():
            presentacionForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Guardado Exitosamente")
            return redirect("consultar_presentacion")
    else:  # GET
        presentacionForm = PresentacionForm
    return render(request, "presentacion/crear_presentacion.html", {"form": presentacionForm})


def consultar_presentacion(request):
    presentaciones = Presentacion.objects.filter(estado=1)
    buscarPresentacion = BuscarPresentacionForm()
    return render(request, "presentacion/consultar_presentacion.html",
                  {"lista_presentaciones": presentaciones, 'buscar_presentacion': buscarPresentacion})

def buscar_presentacion(request):
    global lista_presentaciones, buscarPresentacion
    if request.method == "POST":
        buscarPresentacion = BuscarPresentacionForm(request.POST or None)
        if buscarPresentacion.is_valid():
            ticket = buscarPresentacion.cleaned_data['ticket']
            desde = buscarPresentacion.cleaned_data['desde']
            hasta = buscarPresentacion.cleaned_data['hasta']
            lista_presentaciones = Presentacion.objects.filter(Q(ticket__numticket__exact=ticket) and Q(fecha_creacion__range=(desde, hasta)))
    return render(request, "presentacion/consultar_presentacion.html",
                  {"lista_presentacionesTickets": lista_presentaciones, 'buscar_presentacion': buscarPresentacion})

def exportar_lista_presentacion(request):
    # Create a file-like buffer to receive PDF data.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="exportar_lista_presentacion.pdf"'
    if request.method == "POST":
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch / 4,
                                leftMargin=inch / 4,
                                topMargin=inch / 2,
                                bottomMargin=inch / 4,
                                pagesize=A4)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        presentaciones = []
        styles = getSampleStyleSheet()
        header = Paragraph("Reporte De Presentacion", styles['Heading1'])
        presentaciones.append(header)

        buscarpresentacion = BuscarHorarioForm(request.POST or None)
        if buscarpresentacion.is_valid():
            ticket = buscarpresentacion.cleaned_data['ticket']
            desde = buscarpresentacion.cleaned_data['desde']
            hasta = buscarpresentacion.cleaned_data['hasta']
            lista_presentaciones = Presentacion.objects.filter(Q(ticket__numticket__exact=ticket)) and Q(fecha_creacion__range=(desde, hasta))
            headings = ('fecha', 'Ticket', 'Estado')
            allpresentaciones = [(p.fecha_creacion, p.ticket, p.estado)
                                 for p in lista_presentaciones]

            t = Table([headings] + allpresentaciones)
            t.setStyle(TableStyle(
                [
                    ('GRID', (0, 0), (9, -1), 1, colors.coral),
                    ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
                ]
            ))
            presentaciones.append(t)
            doc.build(presentaciones)
            response.write(buffer.getvalue())
            buffer.close()

    return response

def modificar_presentacion(request, id):
    if request.method == "POST":
        presentacion = get_object_or_404(Presentacion, pk=id)
        presentacionForm = PresentacionForm(request.POST or None, instance=presentacion)
        if presentacionForm.is_valid():
            presentacionForm.save()
            messages.add_message(request, messages.SUCCESS, "Registro Modificado Exitosamente")
            return redirect('consultar_presentacion')
    else:  # GET
        presentacion = get_object_or_404(Presentacion, pk=id)
        presentacionForm = PresentacionForm(instance=presentacion)
    return render(request, "presentacion/modificar_presentacion.html", {'form': presentacionForm})

def eliminar_presentacion(request, id):
    if request.method == "POST":
        presentacion = get_object_or_404(Presentacion, pk=id)
        presentacionForm = PresentacionForm(request.POST or None, instance=presentacion)
        if presentacionForm.is_valid():
            presentacionForm.save(commit=False)
            presentacion.estado = 0
            presentacionForm.save(commit=True)
            messages.add_message(request, messages.SUCCESS, "Registro Eliminado Exitosamente")
            return redirect('consultar_presentacion')
    else:  # GET
        presentacion = get_object_or_404(Presentacion, pk=id)
        presentacionForm = PresentacionForm(instance=presentacion)
    return render(request, "presentacion/eliminar_presentacion.html", {'form': presentacionForm})


# def factura(request):
#     if request.method == "POST":
#         # cb=cabeceraVenta.objects.get(pk=pk)
#         facturacabform = CabeceraVentaForm(request.POST or None)
#         facturadetformset = DetalleFormSet(request.POST or None)
#         if facturacabform.is_valid() and facturadetformset.is_valid():
#             # facturaformset.instance = cb
#             facturadetformset.save()
#             return redirect('consultar_factura')
#     else:
#         facturacabform = CabeceraVentaForm()
#         facturadetformset = DetalleFormSet()
#     return render(request, "factura/factura.html", {'form': facturacabform, 'formdt': facturadetformset})
#
# # def crear_factura(request):
# #     if request.method == "POST":
# #         cabecera = CabeceraVentaForm(request.POST or None)
# #         detalle = DetalleVntForm(request.POST or None)
# #         if cabecera.is_valid():
# #             cabecera.save()
# #             if detalle.is_valid():
# #                 detalle.save()
# #             return redirect('consultar_factura')
# #     else:
# #         cabecera = CabeceraVentaForm(request.POST or None)
# #         detalle = DetalleVntForm(request.POST or None)
# #         detalle_list = list(detalle)
# #     return render(request, "factura/crear_factura.html",
# #                   {'form': cabecera, 'formdt': detalle, 'detalle_list': detalle_list})
#
# def crear_factura(request):
#     if request.method == "POST":
#         facturacabform = CabeceraVentaForm(request.POST or None)
#         facturadetformset = DetalleFormSet(request.POST or None)
#         if facturacabform.is_valid():
#             cb = CabeceraVenta.objects.create(cliente=facturacabform.cleaned_data["cliente"],
#                                               fecha_venta=facturacabform.cleaned_data["fecha_venta"],
#                                               numero_venta=facturacabform.cleaned_data["numero_venta"],
#                                               total_venta=0
#                                               )
#             # cb = facturacabform.save(commit=False)
#             # cb.total_venta_factura = 100
#             # cb = facturacabform.save(commit=True)
#             if facturadetformset.is_valid():
#                 total = 10
#                 for item in facturadetformset.forms:
#                     secuencia = item.cleaned_data.get('secuencia')
#                     producto = item.cleaned_data.get('producto')
#                     presentacion = item.cleaned_data.get('presentacion')
#                     cantidad_venta = item.cleaned_data.get('cantidad_venta')
#                     precio_unitario = item.cleaned_data.get('precio_unitario')
#                     total_venta_producto = item.cleaned_data.get('total_venta_producto')
#                     if producto and presentacion and cantidad_venta and precio_unitario:
#                         amount = float(cantidad_venta) * float(precio_unitario)
#                         total += amount
#                         DetalleVnt(cabecera_venta=cb,
#                                    secuencia=secuencia,
#                                    producto=producto,
#                                    presentacion=presentacion,
#                                    cantidad_venta=cantidad_venta,
#                                    precio_unitario=precio_unitario,
#                                    total_venta_producto=amount).save()
#                 cb.total_venta_factura = total
#                 cb.save()
#         return redirect('consultar_factura')
#     else:
#         facturacabform = CabeceraVentaForm()
#         facturadetformset = DetalleFormSet()
#     return render(request, "factura/crear_factura.html",
#                   {'form': facturacabform, 'formdt': facturadetformset})
#
#
# def modificar_factura(request, id):
#     if request.method == "POST":
#         ticket = get_object_or_404(Ticket, pk=id)
#         ticketform = TicketForm(request.POST or None, instance=ticket)
#         if ticketform.is_valid():
#             ticketform.save()
#             return redirect('consultar_factura')
#     else:
#         ticket = get_object_or_404(Ticket, pk=id)
#         ticketform = TicketForm(instance=ticket)
#     return render(request, "factura/modificar_factura.html", {'form': ticketform})
#
#
# def eliminar_factura(request, id):
#     if request.method == "POST":
#         ticket = get_object_or_404(Ticket, pk=id)
#         ticketform = TicketForm(request.POST or None, instance=ticket)
#         if ticketform.is_valid():
#             ticketform.save(commit=False)
#             ticketform.estado = 0
#             ticketform.save(commit=True)
#             return redirect('consultar_factura')
#     else:
#         ticket = get_object_or_404(Ticket, pk=id)
#         ticketform = TicketForm(instance=ticket)
#     return render(request, "factura/eliminar_factura.html", {'form': ticketform})
#
#
# def consultar_factura(request):
#     buscarFactura = BuscarFacturaForm()
#     facturas = CabeceraVenta.objects.filter(estado=1)
#     return render(request, "factura/consultar_factura.html",
#                   {"lista_facturas": facturas, 'buscar_factura': buscarFactura})


# def buscar_factura(request):
#     if request.method == "POST":
#         buscarFactura = BuscarFacturaForm(request.POST or None)
#         if buscarFactura.is_valid():
#             cliente = buscarFactura.cleaned_data['cliente']
#             numero = buscarFactura.cleaned_data['numero_venta']
#             desde = buscarFactura.cleaned_data['desde']
#             hasta = buscarFactura.cleaned_data['hasta']
#             facturas = CabeceraVenta.objects.filter(
#                 Q(fecha_venta__range=(desde, hasta)) & Q(cliente__nombre__contains=cliente) & Q(
#                     numero_venta__endswith=numero))
#             return render(request, "factura/consultar_factura.html",
#                           {"lista_facturas": facturas, 'buscar_factura': buscarFactura})
#     else:
#         facturas = None
#         buscarFactura = BuscarFacturaForm()
#     return render(request, "factura/consultar_factura.html",
#                   {"lista_facturas": facturas, 'buscar_factura': buscarFactura})


# def buscar_factura(request):
#     global facturas
#     if request.method == "POST":
#         buscarFactura = BuscarFacturaForm(request.POST or None)
#         if buscarFactura.is_valid():
#
#             cliente = buscarFactura.cleaned_data['cliente']
#             numero = buscarFactura.cleaned_data['numero_venta']
#             desde = buscarFactura.cleaned_data['desde']
#             hasta = buscarFactura.cleaned_data['hasta']
#             lista_facturas = CabeceraVenta.objects.filter(
#                 Q(fecha_venta__range=(desde, hasta)) & Q(cliente__nombre__contains=cliente) & Q(
#                     numero_venta__endswith=numero))
#
#             val = buscarFactura.cleaned_data.get("btn")
#             if val == "buscar":
#                 return render(request, "factura/consultar_factura.html",
#                               {"lista_facturas": lista_facturas, 'buscar_factura': buscarFactura})
#             else: #exportar
#                 response = HttpResponse(content_type='application/pdf')
#                 response['Content-Disposition'] = 'filename="exportar_lista_factura.pdf"'
#                 buffer = io.BytesIO()
#
#                 doc = SimpleDocTemplate(buffer,
#                                         rightMargin=inch / 4,
#                                         leftMargin=inch / 4,
#                                         topMargin=inch / 2,
#                                         bottomMargin=inch / 4,
#                                         pagesize=A4)
#                 styles = getSampleStyleSheet()
#                 styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
#                 styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))
#
#                 facturas = []
#                 styles = getSampleStyleSheet()
#                 header = Paragraph("  Reporte de Facturas", styles['Heading1'])
#                 facturas.append(header)
#
#                 #lista_facturas = cabeceraVenta.objects.all()
#                 headings = ('Fecha', 'Cliente', 'Factura', 'Estado')
#                 allfacturas = [(c.fecha_venta, c.cliente, c.numero_venta, c.estado)
#                                for c in lista_facturas]
#                 t = Table([headings] + allfacturas)
#                 t.setStyle(TableStyle(
#                     [
#                         ('GRID', (0, 0), (9, -1), 1, colors.coral),
#                         ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
#                         ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
#                     ]
#                 ))
#                 facturas.append(t)
#                 doc.build(facturas)
#                 response.write(buffer.getvalue())
#                 buffer.close()
#
#             return response
#
#     else: #GET
#         facturas = CabeceraVenta.objects.filter(estado=1)
#         buscarFactura = BuscarFacturaForm()
#     return render(request, "factura/consultar_factura.html",
#                   {"lista_facturas": facturas, 'buscar_factura': buscarFactura})


# def buscar_factura(request):
#     if request.method == "POST":
#         buscarFactura = BuscarFacturaForm(request.POST or None)
#         if buscarFactura.is_valid():
#             cliente = buscarFactura.cleaned_data['cliente']
#             num_factura = buscarFactura.cleaned_data['numero_venta']
#             desde = buscarFactura.cleaned_data['desde']
#             hasta = buscarFactura.cleaned_data['hasta']
#             lista_facturas = factura.objects.filter(
#                 Q(fecha_creacion__range=(desde, hasta)) & Q(cliente__nombre__startswith=cliente) & Q(
#                     num_factura__endswith=num_factura))
#             return render(request, "factura/consultar_factura.html",
#                           {"lista_facturas": lista_facturas, 'buscar_factura': buscarFactura})
#         else:
#             lista_facturas = factura.objects.filter(estado=1)
#             buscarFactura = BuscarFacturaForm()
#         return render(request, "factura/consultar_factura.html",
#                       {"lista_facturas": lista_facturas, 'buscar_factura': buscarFactura})

# def buscar_factura(request, Factura=None):
#     global buscarFactura, facturas
#     if request.method == "POST":
#         buscarFactura = BuscarFacturaForm(request.POST or None)
#         if buscarFactura.is_valid():
#             cliente = buscarFactura.cleaned_data['cliente']
#             num_factura = buscarFactura.cleaned_data['numero_venta']
#             desde = buscarFactura.cleaned_data['desde']
#             hasta = buscarFactura.cleaned_data['hasta']
#             facturas = Factura.objects.filter(Q(cliente__nombre__startswith=cliente) & Q(num_factura__endswith=num_factura) & Q(fecha_creacion__range=(desde, hasta)))
#     return render(request, "factura/consultar_factura.html",
#                   {"lista_facturas": facturas, 'buscar_factura': buscarFactura})

# def buscar_factura(request):
#     global facturas
#     if request.method == "POST":
#         buscarFactura = BuscarFacturaForm(request.POST or None)
#         if buscarFactura.is_valid():
#             cliente = buscarFactura.cleaned_data['cliente']
#             numero = buscarFactura.cleaned_data['numero_venta']
#             desde = buscarFactura.cleaned_data['desde']
#             hasta = buscarFactura.cleaned_data['hasta']
#             facturas = CabeceraVenta.objects.filter(
#                 Q(fecha_venta__range=(desde, hasta)) and Q(cliente__nombre__contains=cliente) and Q(
#                     numero_venta__endswith=numero))
#             return render(request, "factura/consultar_factura.html",
#                           {"lista_facturas": facturas, 'buscar_factura': buscarFactura})
#     else:
#         facturas = CabeceraVenta.objects.filter(estado=1)
#         buscarFactura = BuscarFacturaForm()
#     return render(request, "factura/consultar_factura.html",
#                   {"lista_facturas": facturas, 'buscar_factura': buscarFactura})

# def exportar_lista_factura(request):
#     # Create a file-like buffer to receive PDF data.
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="exportar_lista_factura.pdf"'
#     if request.method == "POST":
#         buffer = io.BytesIO()
#
#         doc = SimpleDocTemplate(buffer,
#                                 rightMargin=inch / 4,
#                                 leftMargin=inch / 4,
#                                 topMargin=inch / 2,
#                                 bottomMargin=inch / 4,
#                                 pagesize=A4)
#
#         styles = getSampleStyleSheet()
#         styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
#         styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))
#
#         facturas = []
#         styles = getSampleStyleSheet()
#         header = Paragraph("  Reporte de Facturas", styles['Heading1'])
#         facturas.append(header)
#
#         buscarFactura = BuscarFacturaForm(request.POST or None)
#         if buscarFactura.is_valid():
#             cliente = buscarFactura.cleaned_data['cliente']
#             numero = buscarFactura.cleaned_data['numero_venta']
#             desde = buscarFactura.cleaned_data['desde']
#             hasta = buscarFactura.cleaned_data['hasta']
#             # lista_facturas = cabeceraVenta.objects.filter(
#             #     Q(fecha_venta__range=(desde, hasta)) & Q(cliente__nombre__contains=cliente) & Q(
#             #         numero_venta__endswith=numero))
#
#             lista_facturas = CabeceraVenta.objects.all()
#             headings = ('Fecha', 'Cliente', 'Factura', 'Estado')
#             allfacturas = [(c.fecha_venta, c.cliente, c.numero_venta, c.estado)
#                            for c in lista_facturas]
#
#             t = Table([headings] + allfacturas)
#             t.setStyle(TableStyle(
#                 [
#                     ('GRID', (0, 0), (9, -1), 1, colors.coral),
#                     ('LINEBELOW', (0, 0), (-1, 0), 2, colors.springgreen),
#                     ('BACKGROUND', (0, 0), (-1, 0), colors.springgreen)
#                 ]
#             ))
#             facturas.append(t)
#             doc.build(facturas)
#             response.write(buffer.getvalue())
#             buffer.close()
#
#     return response


# def ticket_modal(request):
#     global tickets
#     if request.method == "POST":
#         ticketform = BuscarTicketForm(request.POST or None)
#         if ticketform.is_valid():
#             numticket = ticketform.cleaned_data["numticket"]
#             tickets = Ticket.objects.filter(Q(numticket__contains=numticket) & Q(estado__exact=1))
#             # producto = get_object_or_404(Producto, nombre=nombre)
#             # productoform = BuscarProductoForm(instance=producto)
#     else:
#         # productos = Producto.objects.filter(estado=1)
#         tickets = None
#         ticketform = BuscarTicketForm()
#     return render(request, "factura/ticket_modal.html", {"lista_tickets": tickets, 'form': ticketform})
#
#
# def cliente_modal(request):
#     global clientes
#     if request.method == "POST":
#         clienteform = BuscarClienteForm(request.POST or None)
#         if clienteform.is_valid():
#             nombre = clienteform.cleaned_data["nombre"]
#             apellido = clienteform.cleaned_data["apellido"]
#             clientes = Cliente.objects.filter(
#                 Q(nombre__contains=nombre) & Q(apellido__contains=apellido))
#             # producto = get_object_or_404(Producto, nombre=nombre)
#             # productoform = BuscarProductoForm(instance=producto)
#     else:
#         # productos = Producto.objects.filter(estado=1)
#         clientes = None
#         clienteform = BuscarClienteForm()
#     return render(request, "factura/cliente_modal.html", {"lista_clientes": clientes, 'form': clienteform})


# def agregar_ticket_detalle(request, id):
#     global detalle
#     if request.method == "POST":
#         cabecera = CabeceraVentaForm(request.POST or None)
#         if cabecera.is_valid():
#             detalle = DetalleVentaForm(request.POST or None)
#             if detalle.is_valid():
#                 ticket = get_object_or_404(Ticket, pk=id)
#                 dt_nuevo = DetalleVentaForm(instance=ticket)
#                 nuevo = inlineformset_factory(dt_nuevo, extra=1)
#     else:
#         cabecera = CabeceraVentaForm(request.POST or None)
#         detalle = DetalleVentaForm(request.POST or None)
#     return render(request, "factura/crear_factura.html",
#                   {'form': cabecera, 'formdt': detalle})
#
#
# def agregar_cliente(request, id):
#     if request.method == "POST":
#         cabecera = CabeceraVentaForm(request.POST or None)
#         if cabecera.is_valid():
#             cliente = get_object_or_404(Cliente, pk=id)
#             cabecera.cliente = cliente
#             cabecera = CabeceraVentaForm(instance=cabecera)
#     else:
#         cabecera = CabeceraVentaForm()
#     return render(request, "factura//crear_factura.html",
#                   {'form': cabecera})
