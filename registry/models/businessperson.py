from django.db import models
from .person import Person
from .businessperson import BusinessPerson
from valida_doc import validate_cnpj

class BusinessPerson(Person):

    pessoa = models.ForeignKey(
        Person,
        on_delete=models.CASCADE, 
        related_name="businessperson"
    )
    businessperson = models.ForeignKey(
        BusinessPerson, 
        on_delete=models.CASCADE, 
        related_name='BusinessPerson'
    )
    

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
        validate_cnpj(cnpj)
    
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
