from django.db import models

from registry.models.validate_document import ModelABCMeta, ValidateDocument
from .person import Person
import re


class IndividualPerson(Person, ValidateDocument, metaclass=ModelABCMeta):
    _cpf = models.CharField(max_length=14, unique=True)
    _rg = models.CharField(max_length=20, unique=True, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    _pis = models.CharField(max_length=11, unique=True, null=True, blank=True)

    GENDER_CHOICES = [
        (0, "Not Informed"),
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - CPF: {self._cpf}"

    def validate_doc(self, cpf: str) -> bool:
        cpf = re.sub(r"\D", "", cpf)
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
        if not self.validate_doc(cpf):
            raise ValueError("CPF inválido")
        self._cpf = cpf
        self.save()

    def get_cpf(self):
        return self._cpf

    def get_rg(self):
        return self._rg

    def set_rg(self, rg):
        self._rg = rg
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
        return self._pis

    def set_pis(self, pis: str):
        self._pis = pis
        self.save()
