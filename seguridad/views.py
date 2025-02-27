from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets,permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework import status
from django.contrib.auth.models import User
import requests
# Create your views here.
@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'},status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(request.data['password']):
        return Response({'error':'Contraseña Incorrecta'},status=status.HTTP_400_BAD_REQUEST)
    token, created=Token.objects.get_or_create(user=user)
    user_serializer=UserSerializer(instance=user)
    return Response({'user':user_serializer.data,'token':token.key},status=status.HTTP_200_OK)
@api_view(['GET'])
def searchDni(request):
    dni = request.query_params.get('dni', None)
    if(not dni):
        return Response({'error':'Enviar el dni'},status=status.HTTP_400_BAD_REQUEST)
    token='apis-token-13409.TbEsB1se5FUl1A07bYRYIgzDn5qvAnYz=Token Reniec'
    url=f'https://api.apis.net.pe/v2/reniec/dni?numero={dni}'
    headers = {'Content-Type': 'application/json','Authorization': f'Bearer {token}'}
    data=requests.get(url,headers=headers)  
    return Response({'data':data.json()},status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class=UserSerializer
    queryset=User.objects.all().filter(is_active=True).order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(
            username=serializer.validated_data['username'],last_name=serializer.validated_data['last_name'],
            first_name=serializer.validated_data['first_name'],email=serializer.validated_data['email'],
        )
            user.set_password(serializer.validated_data['password'])
            user.is_active=True
            user.save()
            user_serializer=UserSerializer(instance=user)
            return Response({'usuario':user_serializer.data},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    def destroy(self, request, *args, **kwargs):
        obj=self.get_object()
        obj.is_active=False
        obj.save()
        return Response({"data":'Registro Eliminado'},status=status.HTTP_200_OK)
