from django.db import models
import re

class Contact(models.Model):
    id_contact = models.AutoField(primary_key=True)
    contact_choices = [
        ("phone", "Telefone"),
        ("email", "Email")
    ]
    contact_type = models.CharField(max_length=10, choices=contact_choices)
    contact_key = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.contact_key}"
    
    def validate_contact_type(self, contact_type: str):
        if contact_type not in dict(self.contact_choices).keys():
            raise ValueError
        return True
    
    def set_contact_type(self, contact_type: str):
        if self.validate_contact_type(contact_type) is True:
            self.contact_type = contact_type
            self.save()

    def get_contact_type(self):
        return self.contact_type
    
    def validate_contact_key(self, contact_key: str):
        if not contact_key.strip():
            raise ValueError
        if self.contact_type == "phone" and not re.fullmatch(r'\d{8,15}', contact_key):
            raise ValueError
        if self.contact_type == "email" and not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', contact_key):
            raise ValueError
        return True

    def set_contact_key(self, contact_key: str):
        if self.validate_contact_key(contact_key) is True:
            self.contact_key = contact_key
            self.save()

    def get_contact_key(self):
        return self.contact_key

class Municipality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Municipality'
        verbose_name_plural = 'Municipalities'

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
    
    

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

class Address(models.Model):
    # Relationship fields
    person = models.OneToOneField(
        Person, 
        on_delete=models.CASCADE, 
        related_name="address"
    )
    municipality = models.ForeignKey(
        Municipality, 
        on_delete=models.CASCADE, 
        related_name='addresses'
    )
    
    # Address fields
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    neighborhood = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=8)
    
    # Additional useful fields
    is_tax_address = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.street}, {self.number} - {self.municipality.name}"

    @property
    def formatted_address(self):
        parts = [self.street]
        if self.number:
            parts.append(f"nº {self.number}")
        if self.additional_info:
            parts.append(self.additional_info)
        if self.neighborhood:
            parts.append(self.neighborhood)
        parts.append(self.municipality.name)
        parts.append(f"CEP: {self.format_zipcode()}")
        return ", ".join(part for part in parts if part)

    def format_zipcode(self):
        if len(self.zipcode) == 8:
            return f"{self.zipcode[:5]}-{self.zipcode[5:]}"
        return self.zipcode

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['zipcode']),
            models.Index(fields=['is_tax_address']),
             ]
    
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
    
    def get_cpf(self):
        return self.cpf

    def set_cpf(self, cpf):
        self.cpf = cpf
        self.save()

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
