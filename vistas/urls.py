# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("add_vendedor", views.VendedorCreateView.as_view()),
    path("add_vendedor", views.VendedorListView.as_view()),
    path("add_vendedor/<pk>/", views.VendedorUpdateView.as_view, name="actualizar_vendedor"),
    path("add_vendedor/<pk>/", views.VendedorDeleteView.as_view, name="Borrar_vendedor")

]
