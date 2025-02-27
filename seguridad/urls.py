from django.urls import path,include
from .views import *
from rest_framework import routers
router=routers.DefaultRouter()
router.register('usuarios',UserViewSet,basename='seguridad.usuarios')
urlpatterns = [
    path('',include(router.urls)),
    path('login/', login, name='seguridad.login'),
    path('search-dni',searchDni,name='seguridad.buscar-dni')
]
