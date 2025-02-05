from django.db import models
from .municipality import Municipality
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
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        # Primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        d1 = 0 if soma % 11 < 2 else 11 - (soma % 11)
        if int(cpf[9]) != d1:
            return False
        # Segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        d2 = 0 if soma % 11 < 2 else 11 - (soma % 11)
        return int(cpf[10]) == d2
    
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


class BusinessPerson(Person):
    cnpj = models.CharField(max_length=18, unique=True)
    fantasy_name = models.CharField(max_length=255)
    corporate_reason = models.CharField(max_length=255)
    bonds = models.ManyToManyField(Person, related_name="bonds_pj")
    partners = models.ManyToManyField(Person, related_name="partners_pj") 
    opening_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"CNPJ: {self.cnpj}, NOME: {self.fantasy_name}"
    
    def validate_cnpj(self, cnpj: str) -> bool:
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        # Primeiro dígito verificador
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        r = soma % 11
        d1 = 0 if r < 2 else 11 - r
        if int(cnpj[12]) != d1:
            return False
        # Segundo dígito verificador
        pesos2 = [6] + pesos1  # [6,5,4,3,2,9,8,7,6,5,4,3,2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        r = soma % 11
        d2 = 0 if r < 2 else 11 - r
        return int(cnpj[13]) == d2
    
    def set_cnpj(self, cnpj: str):
        if not self.validate_cnpj(cnpj):
            raise ValueError("CNPJ inválido")
        self.cnpj = cnpj
        self.save()
    
    def get_cnpj(self):
        return self.cnpj
    
    def get_fantasy_name(self):
        return self.fantasy_name
    
    def get_corporate_reason(self):
        return self.corporate_reason
    
    def get_bonds(self):
        return self.bonds
    
    def get_partners(self):
        return self.partners
    
    def get_opening_date (self):
        return self.opening_date 
    
    def get_closing_date(self):
        return self.closing_date
