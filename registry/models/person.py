from django.db import models
from .municipality import Municipality
from valida_doc import validate_cpf
import re

class Person(models.Model):
    doc_type = models.CharField(max_length=50)
    doc_id = models.CharField(max_length=50, primary_key=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="people")
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    area_code = models.CharField(max_length=5, null=True, blank=True)
    cellphone = models.CharField(max_length=15, null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_ID(self):
        return self.doc_id

    def get_data_cadastro(self):
        return self.data_cadastro

    def get_nome(self):
        return self.nome

    def get_enderecos(self):
        return self.enderecos.all()

    def get_contatos(self):
        return self.contatos.all()

    def validar_endereco(self, endereco):
        
        if not endereco.logradouro or not endereco.numero or not endereco.bairro or not endereco.cep:
            return False
        
        if not re.match(r'^\d{5}-\d{3}$', endereco.cep):
            return False
        return True

    def validar_contato(self, contato):
      
            tipos_validos = ['email', 'telefone']
      
            if contato.tipo not in tipos_validos:
                return False

            if contato.tipo == 'email' and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contato.chave):
                return False
            if contato.tipo == 'telefone' and not re.match(r'^\+?\d{10,15}$', contato.chave):
                return False
            return True
    
    def add_contato(self, contato):
        if self.validar_contato(contato):
            self.contatos.add(contato)

    def add_endereco(self, endereco):
        if self.validar_endereco(endereco):
            self.enderecos.add(endereco)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


    
class IndividualPerson(Person):
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, unique=True, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    pis = models.CharField(max_length=11, unique=True, null=True, blank=True)

    GENDER_CHOICES = [
        (0, 'Not Informed'),
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other')
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - CPF: {self.cpf}"
    
    def validate_cpf(self, cpf: str) -> bool:
        validate_cpf(cpf)
    
    def set_cpf(self, cpf):
        if not self.validate_cpf(cpf):
            raise ValueError("CPF inválido")
        self.cpf = cpf
        self.save()

    def get_cpf(self):
        return self.cpf

    def get_rg(self):
        return self.rg

    def set_rg(self, rg):
        self.rg = rg
        self.save()  

    def get_name(self):
        return self.name 

    def set_name(self, name):
        self.name = name
        self.save()

    def get_gender(self):
        return self.gender

    def set_gender(self, gender):
        self.gender = gender
        self.save()

    def get_birthday(self):
        return self.birth_date

    def set_birthday(self, birth_date):
        self.birth_date = birth_date
        self.save()
    
    def get_parents(self):
        return {"father": self.father_name, "mother": self.mother_name}

    def set_parents(self, father: str, mother: str):
        self.father_name = father
        self.mother_name = mother
        self.save()
    
    def get_nationality(self):
        return self.nationality
    
    def set_nationality(self, nationality):
        self.nationality = nationality
        self.save()

    def get_pis(self):
        return self.pis

    def set_pis(self, pis: str):
        self.pis = pis
        self.save()


