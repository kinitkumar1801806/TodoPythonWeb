from rest_framework import serializers
from .models import Customers,Moderators,Todos

class CustomersSerializers(serializers.ModelSerializer):
    class Meta:
        model=Customers
        fields='__all__'

class ModeratorsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Moderators
        fields='__all__'

class TodosSerializers(serializers.ModelSerializer):
    class Meta:
        model=Todos
        fields='__all__'