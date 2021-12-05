from django.contrib.auth import decorators
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .forms import DetallePedidoForm, UserRegisterForm, PedidoForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import Categoria, DetallePedido, Pedido, Platillo, Extra

# Create your views here.
@login_required(login_url="/login")
def index(request):

    platillos = list(
        Platillo.objects.order_by("categoria")
    )

    categorias = Categoria.objects.all()

    extras = Extra.objects.all()
    data = {
        "platillos" : platillos,
        "extras" : extras,
        "categorias" : categorias,
    }

    return render(request,"index.html", data)

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            nuevoUsuario = form.save()
            username = form.cleaned_data["username"]
            nombre = form.cleaned_data["firstName"]
            apellido = form.cleaned_data["lastName"]
            password2 = form.cleaned_data["password2"]
            print(password2)
            nuevoUsuario.first_name = nombre
            nuevoUsuario.last_name = apellido
            nuevoUsuario.save()
            nuevoUsuario = authenticate(username = username, password = password2)
            login(request,nuevoUsuario)
            messages.success(request, "Usuario creado")
            return redirect("/")
        else:
            print(form.errors)

    else:
        form = UserRegisterForm()
    context = {"form" : form}
    return render(request, "register.html", context)    

def logout_v(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login")
def ordenes(request): 

    pedidos = Pedido.objects.filter(cliente = request.user)

    detallePedidos = []
    for pedido in pedidos:
        detallePedidos.append(DetallePedido.objects.filter(pedido = pedido))
        
        
    for detallePedidos in detallePedidos: 
        data = {
            "pedido" : detallePedidos
        }

    return render(request,"ordenes.html", data)

@login_required(login_url="/login")
def añadirOrden(request, id):

    if request.method == "POST":
        cantidad = request.POST.get("cantidad")
        descripcion = request.POST.get("descripcion")        
        if not descripcion:
            descripcion = "Nada que mencionar"
        platillo = Platillo.objects.filter(id=id)[0]
        precio = platillo.precio
        total = round(float(cantidad) * precio, 2)
        cliente = request.user
        extras = request.POST.getlist("extras")

        pedido = Pedido(descripcion=descripcion, total=total, cliente=cliente)
        pedido.save()
        detallePedido = DetallePedido(cantidadPlatillos=cantidad, precioPlatillos=precio, estado=False, platillo=platillo, pedido=pedido)

        detallePedido.save() 

        extra = []
        for i in extras:
            extra.append(Extra.objects.filter(id=i)[0])
            
        for i in extra:    
            detallePedido.extras.add(i) 
        
        return redirect("/")
@login_required(login_url="/login")
def listarOrdenes(request):

    detallePedidos = DetallePedido.objects.all()

    data = {
        "pedido" : detallePedidos
    }

    return render(request,"verOrdenes.html", data)
