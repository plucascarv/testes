from django.db import models

class Municipio(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Pessoa(models.Model):
    tipo_doc = models.CharField(max_length=50)
    doc_ident = models.CharField(max_length=50, primary_key=True)
    id_mun = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="pessoas")
    nome = models.CharField(max_length=255)
    dt_nac = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ddd = models.CharField(max_length=5, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    id_pes = models.OneToOneField(Pessoa, on_delete=models.CASCADE, primary_key=True, related_name="endereco")
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.logradouro}, {self.numero}"