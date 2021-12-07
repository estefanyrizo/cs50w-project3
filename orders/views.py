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

    pedido = Pedido.objects.filter(cliente = request.user, estado = False).first()

    data = {
        "pedido" : pedido
    }

    return render(request,"ordenes.html", data)

@login_required(login_url="/login")
def historial(request): 

    pedido = Pedido.objects.filter(cliente = request.user).all()
    data = {
        "pedidos" : pedido
    }

    return render(request,"historial.html", data)

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

        pedido = getOrder(cliente)
        pedido.total += total
        pedido.save()
        detallePedido = DetallePedido(descripcion = descripcion, cantidadPlatillos=cantidad, precioPlatillos=precio, platillo=platillo, pedido=pedido)

        detallePedido.save() 

        extra = []
        for i in extras:
            extra.append(Extra.objects.filter(id=i)[0])
            
        for i in extra:    
            detallePedido.extras.add(i) 
        
        return redirect("/")

def getOrder(user):
    pedido = Pedido.objects.filter(cliente = user, estado = False).first()
    if not pedido:
        pedido = Pedido.objects.create(total=0, cliente=user)
    
    return pedido

@login_required(login_url="/login")
def realizarOrden(request, pedidoPk):
    pedido = Pedido.objects.filter(id = pedidoPk).first()
    pedido.estado = True
    pedido.save()
    messages.success(request, "Pedido realizado")
    return redirect ("/")

@login_required(login_url="/login")
def listarOrdenes(request):

    detallePedidos = DetallePedido.objects.all()

    data = {
        "pedido" : detallePedidos
    }

    return render(request,"verOrdenes.html", data)
