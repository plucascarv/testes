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