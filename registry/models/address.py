from django.db import models
from .person import Person
from .municipality import Municipality

class Address(models.Model):
    # Relationship fields
    pessoa = models.ForeignKey(
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
    classification = models.CharField(max_length=11)
    type = models.CharField(max_length=100)
    
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
    
    # Methods
    def get_classification(self):
        return self.classification
    
    def get_type(self):
        return self.type
    
    def get_street(self):
        return self.street
    
    def get_number(self):
        return self.number
    
    def get_complement(self):
        return self.complement
    
    def get_cep(self):
        return self.cep
    
    def validate_type(self, type: str) -> bool:
        valid_types = ["Residencial", "Comercial", "Industrial"]
        return type in valid_types

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['zipcode']),
            models.Index(fields=['is_tax_address']),
             ]