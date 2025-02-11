from django.db import models
import re

class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=9)

    @staticmethod
    def validar_cep(cep: str):
        padrao_cep = r'^\d{5}-\d{3}$'
        if not re.fullmatch(padrao_cep, cep):
            raise ValueError("CEP inválido")
        return True

    @staticmethod
    def validar_endereco(rua: str, numero: str, cidade: str, estado: str, cep: str):
        if not all([rua.strip(), numero.strip(), cidade.strip(), estado.strip(), cep.strip()]):
            raise ValueError("Todos os campos devem ser preenchidos")
        Endereco.validar_cep(cep)
        return True

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}, CEP: {self.cep}"

# Exemplo de uso
try:
    Endereco.validar_endereco("Rua Exemplo", "123", "Cidade Exemplo", "Estado Exemplo", "12345-678")
    print("Endereço válido!")
except ValueError as e:
    print(f"Endereço inválido: {e}")