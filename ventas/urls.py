from django.urls import path,include
from .views import *
from rest_framework import routers
router=routers.DefaultRouter()
router.register('detalle',VentasViewSet,basename='ventas.ventas')
urlpatterns=[
    path('',include(router.urls)),
    path('resumen/', ResumenDetalleProductosViewSet.as_view(), name='suma-resumen'),
]