from django.urls import reverse_lazy
from ventas.models import Vendedor
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)


class VendedorCreateView(CreateView):
    template_name = "vendedor/add.html"
    model = Vendedor
    Fields = ('__all__')


class VendedorListView(ListView):
    template_name = "vendedor/list.html"
    model = Vendedor


class VendedorUpdateView(UpdateView):
    template_name = "vendedor/update.html"
    model = Vendedor
    Fields = ['nombre',
              'apellido',
              ]
    success_url = reverse_lazy('vendedor_app: correcto')


class VendedorDeleteView(DeleteView):
    template_name = "vendedor/delete.html"
    model = Vendedor
    Fields = ['nombre',
              'apellido',
              ]
    success_url = reverse_lazy('vendedor_app: correcto')
