from rest_framework import serializers
from .models import Municipality, Person, Address, IndividualPerson, BusinessPerson
from .models.individual_person import IndividualPerson


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

# class IndividualSerializer(PersonSerializer):  # Herda de PersonSerializer
#     class Meta:
#         model = IndividualPerson
#         fields = '__all__'
        
class IndividualSerializer(PersonSerializer):  
    class Meta:
        model = IndividualPerson
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        # Exemplo: ocultar CPF e RG para usuários não autenticados
        if request and not request.user.is_authenticated:
            data.pop('cpf', None)
            data.pop('rg', None)
            data.pop('pis', None)

        return data
    

class BusinessSerializer(PersonSerializer):  # Herda de PersonSerializer
    class Meta:
        model = businessperson.BusinessPerson
        fields = '__all__'
        