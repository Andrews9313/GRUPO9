# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    ## CRUD PARA CLIENTE
    path("crear_cliente", views.crear_cliente, name="crear_cliente"),
    path("modificar_cliente<int:id>", views.modificar_cliente, name="modificar_cliente"),
    path("eliminar_cliente<int:id>", views.eliminar_cliente, name="eliminar_cliente"),
    path("consultar_cliente", views.consultar_cliente, name="consultar_cliente"),
    path('buscar_cliente', views.buscar_cliente, name="buscar_cliente"),
    path('exportar_lista_cliente', views.exportar_lista_cliente, name="exportar_lista_cliente"),

    ## CRUD PARA DETALLE_VENTA
    path("crear_detalleventa", views.crear_detalleventa, name="crear_detalleventa"),
    path("modificar_detalleventa<int:id>", views.modificar_detalleventa, name="modificar_detalleventa"),
    path("eliminar_detalleventa<int:id>", views.eliminar_detalleventa, name="eliminar_detalleventa"),
    path("consultar_detalleventa", views.consultar_detalleventa, name="consultar_detalleventa"),
    path('buscar_detalleventa', views.buscar_detalleventa, name="buscar_detalleventa"),
    path('exportar_lista_detalleventa', views.exportar_lista_detalleventa, name="exportar_lista_detalleventa"),

    ## CRUD PARA TICKET
    path("crear_ticket/", views.crear_ticket, name="crear_ticket"),
    path("modificar_ticket<int:id>/", views.modificar_ticket, name="modificar_ticket"),
    path("eliminar_ticket<int:id>/", views.eliminar_ticket, name="eliminar_ticket"),
    path("consultar_ticket/", views.consultar_ticket, name="consultar_ticket"),
    path('buscar_ticket/', views.buscar_ticket, name="buscar_ticket"),
    # path('lista_tickets/', views.lista_tickets, name="lista_tickets"),
    path('exportar_lista_ticket', views.exportar_lista_ticket, name="exportar_lista_ticket"),

    ## CRUD PARA VENTA
    path("crear_venta/", views.crear_venta, name="crear_venta"),
    path("modificar_venta<int:id>/", views.modificar_venta, name="modificar_venta"),
    path("eliminar_venta<int:id>/", views.eliminar_venta, name="eliminar_venta"),
    path("consultar_venta/", views.consultar_venta, name="consultar_venta"),
    path('buscar_venta/', views.buscar_venta, name="buscar_venta"),
    path('exportar_lista_venta', views.exportar_lista_venta, name="exportar_lista_venta"),

    ## CRUD PARA PRESENTACION
    path("crear_presentacion", views.crear_presentacion, name="crear_presentacion"),
    path("modificar_presentacion<int:id>", views.modificar_presentacion, name="modificar_presentacion"),
    path("eliminar_presentacion<int:id>", views.eliminar_presentacion, name="eliminar_presentacion"),
    path("consultar_presentacion", views.consultar_presentacion, name="consultar_presentacion"),
    path('buscar_presentacion', views.buscar_presentacion, name="buscar_presentacion"),
    path('exportar_lista_presentacion', views.exportar_lista_presentacion, name="exportar_lista_presentacion"),

    ## CRUD PARA METODO DE PAGO
    path("crear_metodopago/", views.crear_metodopago, name="crear_metodopago"),
    path("modificar_metodopago/<int:id>", views.modificar_metodopago, name="modificar_metodopago"),
    path("eliminar_metodopago/<int:id>", views.eliminar_metodopago, name="eliminar_metodopago"),
    path("consultar_metodopago/", views.consultar_metodopago, name="consultar_metodopago"),
    path('buscar_metodopago/', views.buscar_metodopago, name="buscar_metodopago"),
    path('exportar_lista_metodopago', views.exportar_lista_metodopago, name="exportar_lista_metodopago"),

    ## CRUD PARA VENDEDOR
    path("crear_vendedor/", views.crear_vendedor, name="crear_vendedor"),
    path("modificar_vendedor/<int:id>", views.modificar_vendedor, name="modificar_vendedor"),
    path("eliminar_vendedor/<int:id>", views.eliminar_vendedor, name="eliminar_vendedor"),
    path("consultar_vendedor/", views.consultar_vendedor, name="consultar_vendedor"),
    path('buscar_vendedor', views.buscar_vendedor, name="buscar_vendedor"),
    path('exportar_lista_vendedor', views.exportar_lista_vendedor, name="exportar_lista_vendedor"),

    ## CRUD PARA SALA
    path("crear_sala/", views.crear_sala, name="crear_sala"),
    path("modificar_sala/<int:id>", views.modificar_sala, name="modificar_sala"),
    path("eliminar_sala/<int:id>", views.eliminar_sala, name="eliminar_sala"),
    path("consultar_sala/", views.consultar_sala, name="consultar_sala"),
    path('buscar_sala/', views.buscar_sala, name="buscar_sala"),
    path('exportar_lista_sala', views.exportar_lista_sala, name="exportar_lista_sala"),

    ## CRUD PARA ASIENTO
    path("crear_asiento/", views.crear_asiento, name="crear_asiento"),
    path("modificar_asiento/<int:id>", views.modificar_asiento, name="modificar_asiento"),
    path("eliminar_asiento/<int:id>", views.eliminar_asiento, name="eliminar_asiento"),
    path("consultar_asiento/", views.consultar_asiento, name="consultar_asiento"),
    path('buscar_asiento/', views.buscar_asiento, name="buscar_asiento"),
    path('exportar_lista_asiento', views.exportar_lista_asiento, name="exportar_lista_asiento"),

    ## CRUD PARA PROMOCION
    path("crear_promocion/", views.crear_promocion, name="crear_promocion"),
    path("modificar_promocion/<int:id>", views.modificar_promocion, name="modificar_promocion"),
    path("eliminar_promocion/<int:id>", views.eliminar_promocion, name="eliminar_promocion"),
    path("consultar_promocion/", views.consultar_promocion, name="consultar_promocion"),
    path('buscar_promocion/', views.buscar_promocion, name="buscar_promocion"),
    path('exportar_lista_promocion', views.exportar_lista_promocion, name="exportar_lista_promocion"),

    ## CRUD PARA PELICULA
    path("crear_pelicula/", views.crear_pelicula, name="crear_pelicula"),
    path("modificar_pelicula/<int:id>", views.modificar_pelicula, name="modificar_pelicula"),
    path("eliminar_pelicula/<int:id>", views.eliminar_pelicula, name="eliminar_pelicula"),
    path("consultar_pelicula/", views.consultar_pelicula, name="consultar_pelicula"),
    path('buscar_pelicula/', views.buscar_pelicula, name="buscar_pelicula"),
    path('exportar_lista_pelicula', views.exportar_lista_pelicula, name="exportar_lista_pelicula"),

    ## CRUD PARA CATEGORIA
    path("crear_categoria/", views.crear_categoria, name="crear_categoria"),
    path("modificar_categoria/<int:id>", views.modificar_categoria, name="modificar_categoria"),
    path("eliminar_categoria/<int:id>", views.eliminar_categoria, name="eliminar_categoria"),
    path("consultar_categoria/", views.consultar_categoria, name="consultar_categoria"),
    path('buscar_categoria/', views.buscar_categoria, name="buscar_categoria"),
    path('exportar_lista_categoria', views.exportar_lista_categoria, name="exportar_lista_categoria"),

    ## CRUD PARA CARTELERA
    path("crear_cartelera/", views.crear_cartelera, name="crear_cartelera"),
    path("modificar_cartelera/<int:id>", views.modificar_cartelera, name="modificar_cartelera"),
    path("eliminar_cartelera/<int:id>", views.eliminar_cartelera, name="eliminar_cartelera"),
    path("consultar_cartelera/", views.consultar_cartelera, name="consultar_cartelera"),
    path('buscar_cartelera/', views.buscar_cartelera, name="buscar_cartelera"),
    path('exportar_lista_cartelera', views.exportar_lista_cartelera, name="exportar_lista_cartelera"),

    ## CRUD PARA HORARIO
    path("crear_horario/", views.crear_horario, name="crear_horario"),
    path("modificar_horario/<int:id>", views.modificar_horario, name="modificar_horario"),
    path("eliminar_horario/<int:id>", views.eliminar_horario, name="eliminar_horario"),
    path("consultar_horario/", views.consultar_horario, name="consultar_horario"),
    path('buscar_horario', views.buscar_horario, name="buscar_horario"),
    path('exportar_lista_horario', views.exportar_lista_horario, name="exportar_lista_horario"),

    # ## CRUD FACTURA
    # path('buscar_factura/', views.buscar_factura, name="buscar_factura"),
    # path('exportar_lista_factura', views.exportar_lista_factura, name="exportar_lista_factura"),
    # path('crear_factura/', views.crear_factura, name="crear_factura"),
    # path('factura/', views.factura, name="factura"),
    # path('modificar_factura/<int:id>', views.modificar_factura, name="modificar_factura"),
    # path('eliminar_factura/<int:id>', views.eliminar_factura, name="eliminar_factura"),
    # path('consultar_factura/', views.consultar_factura, name="consultar_factura"),
    # path('ticket_modal/', views.ticket_modal, name="ticket_modal"),
    # path('cliente_modal/', views.cliente_modal, name="cliente_modal"),
    # path('agregar_ticket_detalle/<int:id>', views.agregar_ticket_detalle, name="agregar_ticket_detalle"),
    # path('agregar_cliente/<int:id>', views.agregar_cliente, name="agregar_cliente"),


]
