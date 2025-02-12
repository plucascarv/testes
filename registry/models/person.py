from django.db import models
from registry.models.address import Address, LeanAddress
from registry.models.contact import Contact
from registry.models.validate_contact import ContactImplementation


class Person(models.Model):
    doc_type = models.CharField(max_length=50)
    doc_id = models.CharField(max_length=50, primary_key=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="people"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="people"
    )
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

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_contatos(self):
        return self.contact

    def add_contact(self, contact_key: str, contact_type: str):
        if ContactImplementation.validate_contact_key(
            contact_key, contact_type
        ):
            target = Person.objects.get(name=self.name)
            newContact = Contact.objects.create(
                contact_key=contact_key,
                contact_type=contact_type,
                person=target,
            )
            newContact.save()

    def add_address(self, address: LeanAddress):
        if Address.validate_address(**address):
            target = Person.objects.get(name=self.name)
            newAddress = Address.objects.create(person=target, **address)
            newAddress.save()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
