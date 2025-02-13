from rest_framework import serializers
from .models import *

class ProducotosSerializer(serializers.ModelSerializer):
    class Meta:
        model=Productos
        fields='__all__'