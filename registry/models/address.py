import re
from typing import TypedDict
from django.db import models
from .person import Person
from .municipality import Municipality


class LeanAddress(TypedDict):
    street_name: str
    street_number: str
    city_name: str
    state_name: str
    zip_code: str


class Address(models.Model):
    # Relationship fields
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="address"
    )
    municipality = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, related_name="addresses"
    )

    # Address fields
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    additional_info = models.CharField(max_length=255, null=True, blank=True)
    neighborhood = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=8)
    classification = models.CharField(max_length=11)
    address_type = models.CharField(max_length=100)

    # Additional useful fields
    is_tax_address = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.street_name}, {self.street_number} - "
            f"{self.municipality.city_name}"
        )

    @property
    def formatted_address(self):
        parts = [self.street_name]
        if self.street_number:
            parts.append(f"nº {self.street_number}")
        if self.additional_info:
            parts.append(self.additional_info)
        if self.neighborhood:
            parts.append(self.neighborhood)
        parts.append(self.municipality.city_name)
        parts.append(f"CEP: {self.formatted_zipcode()}")
        return ", ".join(part for part in parts if part)

    def formatted_zipcode(self):
        if len(self.zip_code) == 8:
            return f"{self.zip_code[:5]}-{self.zip_code[5:]}"
        return self.zip_code

    # Methods
    def get_classification(self):
        return self.classification

    def get_type(self):
        return self.address_type

    def get_street(self):
        return self.street_name

    def get_number(self):
        return self.street_number

    def get_additional_info(self):
        return self.additional_info

    def get_zip_code(self):
        return self.zip_code

    def validate_type(self, type: str) -> bool:
        valid_types = ["Residencial", "Comercial", "Industrial"]
        return type in valid_types

    @staticmethod
    def validate_zip_code(checkable_zip_code: str):
        zip_code_pattern = r"^\d{5}-\d{3}$"
        if not re.fullmatch(zip_code_pattern, checkable_zip_code):
            raise ValueError("CEP inválido")
        return True

    @staticmethod
    def validate_address(
        street_name: str,
        street_number: str,
        city_name: str,
        state_name: str,
        zip_code: str,
    ):
        if not all(
            [
                street_name.strip(),
                street_number.strip(),
                city_name.strip(),
                state_name.strip(),
                zip_code.strip(),
            ]
        ):
            raise ValueError("Todos os campos devem ser preenchidos")
        Address.validate_zip_code(zip_code)
        return True

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["zipcode"]),
            models.Index(fields=["is_tax_address"]),
        ]
