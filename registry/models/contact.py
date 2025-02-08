from django.db import models
import re

class ContactImplementation(models.Model):
    contact_choices = {
        "phone": r'\d{8,15}',
        "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        }

    @staticmethod
    def validate_contact_type(contact_type:str):
        if contact_type not in ContactImplementation.contact_choices.keys():
            raise ValueError
        return True
    
    @staticmethod
    def validate_contact_key(contact_key:str, contact_type:str):
        aux = ContactImplementation.contact_choices.get(contact_type)
        if (aux and not re.fullmatch(aux, contact_key)) or not contact_key.strip():
            raise ValueError
        return True


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
    
    def set_contact_type(self, contact_type: str):
        if ContactImplementation.validate_contact_type(contact_type):
            self.contact_type = contact_type
            self.save()

    def get_contact_type(self):
        return self.contact_type

    def set_contact_key(self, contact_key: str):
        if ContactImplementation.validate_contact_key(contact_key, self.contact_type):
            self.contact_key = contact_key
            self.save()

    def get_contact_key(self):
        return self.contact_key
