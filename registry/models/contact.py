from django.db import models
from .validate_contact import ContactImplementation


class Contact(models.Model):
    id_contact = models.AutoField(primary_key=True)
    contact_choices = [("phone", "Telefone"), ("email", "Email")]
    contact_type = models.CharField(max_length=10, choices=contact_choices)
    contact_key = models.CharField(max_length=50, null=False, blank=False)

    def __init__(self, contact_type, contact_key) -> None:
        self.contact_type = contact_type
        self.contact_key = contact_key

    def __str__(self):
        return f"{self.contact_key}"

    def set_contact_type(self, contact_type: str):
        if ContactImplementation.validate_contact_type(contact_type):
            self.contact_type = contact_type
            self.save()

    def get_contact_type(self):
        return self.contact_type

    def set_contact_key(self, contact_key: str):
        if ContactImplementation.validate_contact_key(
            contact_key, self.contact_type
        ):
            self.contact_key = contact_key
            self.save()

    def get_contact_key(self):
        return self.contact_key

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
