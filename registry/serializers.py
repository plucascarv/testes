from rest_framework import serializers
from .models import Municipio, Pessoa, Endereco, PessoaFisica, PessoaJuridica

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class PessoaFisicaSerializer(PessoaSerializer):  # Herda de PessoaSerializer
    class Meta:
        model = PessoaFisica
        fields = '__all__'

class PessoaJuridicaSerializer(PessoaSerializer):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'