from rest_framework import serializers
from .models import Municipality, Person, Address, IndividualPerson, BusinessPerson


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class IndividualSerializer(PersonSerializer):  # Herda de PersonSerializer
    class Meta:
        model = IndividualPerson
        fields = '__all__'


class BusinessSerializer(PersonSerializer):  # Herda de PersonSerializer
    class Meta:
        model = BusinessPerson
        fields = '__all__'
        