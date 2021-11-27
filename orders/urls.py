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
    path("verordenes", views.verOrdenes, name = "verordenes"),
    path("añadirorden/<id>", views.añadirOrden, name = "añadirorden")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
