from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from .serializers import *
from rest_framework.authentication import TokenAuthentication
# Create your views here.
class ProductosViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    queryset=Productos.objects.all().filter(estado=True).order_by('-id')
    permission_classes=[
        permissions.AllowAny,
    ]
    serializer_class = ProducotosSerializer
    def perform_create(self, serializer):
        print("Request data:", self.request.data.get('id'))
    # Crear una copia mutable de los datos del request
        data = self.request.data.copy()
        data['id_tipo_productos'] = 123  # Agrega el nuevo valor aquí (cámbialo según sea necesario)
       
        obj = Productos.objects.filter(id=data.get('id')).first()

        if obj:
        # Actualizar objeto existente
            for attr, value in serializer.validated_data.items():
                setattr(obj, attr, value)
            obj.estado = True  # Asegura que el estado sea True en la actualización
            obj.save()
            serializer.instance = obj  # Asigna el objeto actualizado al serializer
        else:
        # Serializar los datos con la modificación incluida
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)  # Validar los datos
            producto=serializer.save(estado=True)  # Guardar el nuevo producto
            inventario={'cantidad':data.get('stock'),'id_producto':producto.id}
            serializer_inventario=InventarioSerializer(data=inventario)
            if(serializer_inventario.is_valid()):
                serializer_inventario.save(estado=True)
            else:
                raise serializers.ValidationError(detalle_serializer.errors)

    def destroy(self, request, *args, **kwargs):
        obj=self.get_object()
        obj.estado=False
        obj.save()
        return Response(data=status.HTTP_200_OK)
class InventariosViewSet(viewsets.ModelViewSet):
    queryset=Inventarios.objects.all().filter(estado=True).order_by('-id')
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    serializer_class=InventarioSerializer
    def perform_create(self, serializer):
        data=self.request.data.copy()
        serializer=self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)  # Validar los datos
        inventario=serializer.save(estado=True)
        producto=Productos.objects.get(id=data.get('id_producto'))
        if producto:
            producto.stock=int(data.get('cantidad'))+producto.stock
            producto.save()
        else:
            return Response('Producto no encontrado',status=status.HTTP_400_BAD_REQUEST)
        return Response(data=status.HTTP_200_OK)