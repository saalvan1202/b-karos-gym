from django.db import models
from django.utils import timezone
# Create your models here.
class Productos(models.Model):
    nombre=models.CharField(max_length=50,unique=False,null=False,blank=True)
    stock=models.IntegerField(blank=True,unique=False,null=False)
    precio=models.DecimalField(max_digits=10,decimal_places=2,blank=True,unique=False,null=False)
    id_tipo_productos=models.IntegerField(blank=True,unique=False,null=False)
    estado=models.BooleanField(blank=True,unique=False,null=False)

    class Meta:
        db_table='productos'

class Inventarios(models.Model):
    cantidad=models.IntegerField(blank=True,unique=False,null=False)
    fecha=models.DateTimeField(blank=True,unique=False,null=True,default=timezone.now)
    id_producto=models.IntegerField(blank=True,unique=False,null=False)
    estado=models.BooleanField(blank=True,unique=False,null=False)

    class Meta:
        db_table='inventarios'