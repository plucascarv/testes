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
