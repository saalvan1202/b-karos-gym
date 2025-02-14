from django.shortcuts import render
from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from .serializers import *
# Create your views here.
class ProductosViewSet(viewsets.ModelViewSet):
    queryset=Productos.objects.all().filter(estado=True)
    permission_classes=[
        permissions.AllowAny,
    ]
    serializer_class = ProducotosSerializer
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        obj=Productos.objects.filter(id=request.data.get('id')).first()    
        if(obj):
            for attr, value in serializer.validated_data.items():
                setattr(obj, attr, value)
            obj.estado = True # Asegura que el estado sea True en la actualización
            obj.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Crear (no se proporcionó ID)
            serializer.save(estado=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
    def destroy(self, request, *args, **kwargs):
        obj=self.get_object()
        obj.estado=False
        obj.save()
        return Response(data=status.HTTP_200_OK)