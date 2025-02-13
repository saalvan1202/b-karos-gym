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
    def perform_create(self, serializer):
        print("Request data:", self.request.data.get('id'))
        obj=Productos.objects.filter(id=self.request.data.get('id')).first()    
        if(obj):
            for attr, value in serializer.validated_data.items():
                setattr(obj, attr, value)
            obj.estado = True # Asegura que el estado sea True en la actualización
            obj.save()
        else:
            # Crear (no se proporcionó ID)
            serializer.save(estado=True)
    def destroy(self, request, *args, **kwargs):
        obj=self.get_object()
        obj.estado=False
        obj.save()
        return Response(data=status.HTTP_200_OK)