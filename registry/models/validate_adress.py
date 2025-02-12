from django.db import models
import re


class Address(models.Model):
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10)
    city_name = models.CharField(max_length=100)
    state_name = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=9)

    @staticmethod
    def validate_zip_code(cep: str):
        zip_code_pattern = r"^\d{5}-\d{3}$"
        if not re.fullmatch(zip_code_pattern, cep):
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

    def __str__(self):
        return (
            f"{self.street_name}, {self.street_number} - "
            f"{self.city_name}/{self.state_name}, CEP: {self.zip_code}"
        )


# Exemplo de uso
try:
    Address.validate_address(
        "Rua Exemplo", "123", "Cidade Exemplo", "Estado Exemplo", "12345-678"
    )
    print("Endereço válido!")
except ValueError as e:
    print(f"Endereço inválido: {e}")
