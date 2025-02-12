import re
from django.db import models
from .businessperson import BusinessPerson
from .person import Person
from registry.models.validate_document import ModelABCMeta, ValidateDocument


class BusinessPerson(Person, ValidateDocument, metaclass=ModelABCMeta):

    pessoa = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="businessperson"
    )
    businessperson = models.ForeignKey(
        BusinessPerson, on_delete=models.CASCADE, related_name="BusinessPerson"
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

    def validate_doc(self, cnpj: str) -> bool:
        cnpj = re.sub(r"\D", "", cnpj)
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
        if not self.validate_doc(cnpj):
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

    def get_opening_date(self):
        return self.opening_date

    def get_closing_date(self):
        return self.closing_date
