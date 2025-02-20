from rest_framework import serializers
from .models import *
from inventario.serializers import ProducotosSerializer
class VentasSerializers(serializers.ModelSerializer):
    fecha_formateada=serializers.SerializerMethodField()
    hora_formateada=serializers.SerializerMethodField()
    class Meta:
        model=Ventas
        fields=['total','fecha','usuario_responsable','estado','id','fecha_formateada','hora_formateada']
    def get_fecha_formateada(self, obj):
        return obj.fecha_formateada()
    def get_hora_formateada(self,obj):
        return obj.hora_formateada()
class DetalleVentasSerializers(serializers.ModelSerializer):
    nombre = serializers.CharField(source='producto.nombre', read_only=True)
    stock=serializers.CharField(source='producto.stock', read_only=True)
    class Meta:
        model=DetallesVentas
        fields=['id', 'id_venta', 'nombre', 'cantidad', 'precio_unitario', 'sub_total','producto','stock','estado']
class CortesiasSerializers(serializers.ModelSerializer):
    class Meta:
        model=Cortesias
        fields='__all__'