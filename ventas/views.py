from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,permissions,status
from .serializers import *
from django.db import transaction
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
                            print(f"Detalle data: {detalle}") 
                            if(detalle):
                                detalle_serializer=DetalleVentasSerializers(detalle,data=detalle_data,partial=True)
                                
                                if detalle_serializer.is_valid():
                                    print(f"Detalle data:") 
                                    detalle_serializer.save()
                                else:
                                    raise serializers.ValidationError(detalle_serializer.errors) 
                            else:
    
                                detalle_serializer = DetalleVentasSerializers(data=detalle_data)
                                if detalle_serializer.is_valid():
                                    detalle_serializer.save()
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