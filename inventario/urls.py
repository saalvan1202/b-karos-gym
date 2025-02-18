from rest_framework import routers
from .views import *
from django.urls import path,include

router=routers.DefaultRouter()
router.register('productos',ProductosViewSet,basename='inventario.productos')
router.register('inventarios',InventariosViewSet,basename='inventario.inventarioss')

urlpatterns=[
    path('',include(router.urls))
]