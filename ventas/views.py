from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import TruncDate
from rest_framework import viewsets,permissions,status
from .serializers import *
from inventario.models import *
from django.db import transaction
from django.db.models import Sum,F
from datetime import date
# Create your views here.
class VentasViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class = VentasSerializers
    queryset = Ventas.objects.all().filter(estado=True).order_by('-id')
    def retrieve(self, request, *args, **kwargs): 
         instance=self.get_object()
         venta=self.get_serializer(instance).data
         data=DetallesVentas.objects.filter(id_venta=venta['id'])
         detalles=DetalleVentasSerializers(data,many=True).data
         venta['detalles']=detalles
         return Response(venta, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    venta_id=request.data.get('id')
                    if(venta_id):
                        venta=Ventas.objects.filter(id=venta_id).first()
                        if(venta):
                            serializer=self.get_serializer(venta,data=request.data,partial=True)
                            if serializer.is_valid():
                                venta=serializer.save()
                            else:
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            venta = serializer.save()  # Guarda la venta
                    # Crear los detalles de la venta
                    for detalle_data in request.data.get('detalles', []): # Manejar la ausencia de 'detalles'
                        print(f"Detalle data: {detalle_data}") 
                        detalle_data['id_venta']=venta.id
                        detalle_id=detalle_data['id']
                        if(detalle_id):
                            detalle=DetallesVentas.objects.filter(id=detalle_id).first()
                            if(detalle):
                                detalle_cantidad=detalle.cantidad
                                detalle_serializer=DetalleVentasSerializers(detalle,data=detalle_data,partial=True)
                                if detalle_serializer.is_valid():
                                    detalle_serializer.save()
                                    producto=Productos.objects.get(id=detalle_data.get('producto'))
                                    if(producto):
                                        producto.stock=(producto.stock+detalle_cantidad)-int(detalle_data.get('cantidad'))
                                        print(producto.stock)
                                        producto.save()
                                    else:
                                        print('Producto no encontrado')   
                                else:
                                    raise serializers.ValidationError(detalle_serializer.errors) 
                            else:
    
                                detalle_serializer = DetalleVentasSerializers(data=detalle_data)
                                if detalle_serializer.is_valid():
                                    detalle_serializer.save()
                                    #Restamos lo vendido
                                    producto=Productos.objects.get(id=detalle_data.get('producto'))
                                    if(producto):
                                        producto.stock=producto.stock-int(detalle_data.get('cantidad'))
                                        producto.save()
                                    else:
                                        print('no')
                                else:
                                    raise serializers.ValidationError(detalle_serializer.errors) # Revertir si hay errores en los detalles

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) # Capturar y mostrar errores

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        obj=self.get_object()
        obj.estado=False
        obj.save()
        return Response(data=status.HTTP_200_OK)
    
class ResumenDetalleProductosViewSet(APIView):
   def get(self, request, *args, **kwargs):
       fecha=request.query_params.get('fecha',date.today())
       response=DetallesVentas.objects.filter(id_venta__fecha__date=fecha).values(nombre=F('producto__nombre')).annotate(SumCantidad=Sum('cantidad'))
       if(response):
        return Response(list(response), status=status.HTTP_201_CREATED)
       else:
        return Response('No hay datos',status=status.HTTP_201_CREATED)
       
       
      
    