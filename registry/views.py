from django.shortcuts import render

from rest_framework import viewsets
from .models import Municipality, Person, Address
from .serializers import MunicipalitySerializer, PersonSerializer, AddressSerializer

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer


class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
