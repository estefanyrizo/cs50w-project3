from django.db import models
from django.db.models.deletion import PROTECT

# Create your models here.

class Categoria(models.Model):
    categorias = models.CharField(max_length=30)
    def __str__(self):
        return f"Hemos agregado esta categoria: {self.categorias}"

class Extra(models.Model):
    nombre = models.CharField(max_length=20)
    def __str__(self):
        return f"Hemos agregado este topin: {self.nombre}"    
    
class Platillo(models.Model):
    nombre = models.CharField(max_length=40)
    maxExtras = models.IntegerField()
    precio = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to="platillos", null=True)
    def __str__(self):
        return f"Hemos agregado este platillo: {self.nombre}"

class Pedido(models.Model):
    descripcion = models.CharField(max_length=50)
    total = models.FloatField()
    id_user = models.ForeignKey(Categoria, on_delete=models.PROTECT)

class DetallePedido(models.Model):
    cantidadPlatillos = models.IntegerField()
    precioPlatillos = models.FloatField()
    cantidadExtras = models.IntegerField()
    id_platillo = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    id_extras = models.ManyToManyField(Extra, blank=True)
