from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from inventario.views import Productos
# Create your models here.
class Ventas(models.Model):
    total=models.DecimalField(max_digits=10,decimal_places=2,blank=True,unique=False,null=False)
    usuario_responsable=models.CharField(max_length=50,blank=True,unique=False,null=True)
    fecha=models.DateTimeField(blank=True,unique=False,null=True,default=timezone.now)
    estado=models.BooleanField(blank=True,unique=False,null=False,default=True)
    def fecha_formateada(self):
        return localtime(self.fecha).strftime('%d/%m/%Y')
    def hora_formateada(self):
        return localtime(self.fecha).strftime('%H:%M:%S')
    class Meta:
        db_table='ventas'
    
class DetallesVentas(models.Model):
    cantidad=models.IntegerField(blank=True,unique=False,null=False)
    precio_unitario=models.DecimalField(max_digits=10,decimal_places=2,blank=True,unique=False,null=False)
    sub_total=models.DecimalField(max_digits=10,decimal_places=2,blank=True,unique=False,null=False)
    id_venta=models.ForeignKey(Ventas, on_delete=models.CASCADE, db_column='id_venta')
    producto=models.ForeignKey(Productos, on_delete=models.CASCADE)
    class Meta:
        db_table='detalles_ventas'