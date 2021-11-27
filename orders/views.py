from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import DetallePedido, Platillo

# Create your views here.
@login_required(login_url="/login")
def index(request):
    platillos = Platillo.objects.all()
    data = {
        "platillos" : platillos
    }
    return render(request,"index.html", data)

""" def logins(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(to="index")
            
        else:
           print("No sirve")

    return render(request, "login.html")
 """

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
            nuevoUsuario = authenticate(username = username, first_name = nombre, last_name = apellido, password = password2)
            login(request,nuevoUsuario)
            messages.success(request, "Usuario creado")
            return redirect("/")

    else:
        form = UserRegisterForm()
    context = {"form" : form}
    return render(request, "register.html", context)    

def logout_v(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login")
@permission_required('app.view_detallepedido')
def verOrdenes(request): 
    return render(request,"ordenes.html")

@login_required(login_url="/login")
def añadirOrden(request, id):

    platillos = Platillo.objects.filter(id=id)
    data = {
        "platillos" : platillos
    }

    return render(request, "añadirOrden.html", data)
        