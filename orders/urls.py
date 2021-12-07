from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", LoginView.as_view(template_name = "login.html"), name = "login"),
    path("register", views.register, name = "register"),
    path("logout", LogoutView.as_view(template_name = "logout.html"), name = "logout"),
    path("ordenes", views.ordenes, name = "ordenes"),
    path("añadirorden/<id>", views.añadirOrden, name = "añadir-orden"),
    path("listar-ordenes", views.listarOrdenes, name = "listar-ordenes"),
    path("realizar-orden/<pedidoPk>", views.realizarOrden, name = "realizar-orden"),
    path("historial", views.historial, name="historial")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
