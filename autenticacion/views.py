from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm

# Create your views here.
from .models import Usuario


def crear_usuario(request):
    if request.method == "POST":
        usuarioForm =  UsuarioForm(request.POST or None)
        if usuarioForm.is_valid():
            usuarioForm.save()
            return redirect ("consulta_usuario")
    else:
        usuarioForm = UsuarioForm()
    return render(request, "crear_usuario.html", {'form':usuarioForm})



def eliminar_usuario(request, id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm =  UsuarioForm(request.POST or None, instance=usuario)
        if usuarioForm.is_valid():
            usuarioForm.save()
            return redirect ("consulta_usuario")
    else:
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm = UsuarioForm(instance=usuario)
    return render(request, "eliminar_usuario.html", {'form':usuarioForm})


def modificar_usuario(request, id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm = UsuarioForm(request.POST or None, instance=usuario)
        if usuarioForm.is_valid():
            usuarioForm.save()
            return redirect ("consulta_usuario")
    else:
        usuario = get_object_or_404(Usuario, pk=id)
        usuarioForm = UsuarioForm(instance=usuario)
    return render(request, "modificar_usuario.html", {'form':usuarioForm})


def consulta_usuario(request):
    lista_usuarios = Usuario.objects.filter(estado=1)

    return render(request, "consulta_usuario.html", {'lista_usuarios':lista_usuarios})