from django.db import models
import re

class Contato(models.Model):
    id_contato = models.AutoField(primary_key=True)
    contato_escolhas = [
        ("telefone", "Telefone"),
        ("email", "Email")
    ]
    tipo = models.CharField(max_length=10, choices=contato_escolhas)
    chave = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.chave}"
    
    def validar_tipo(self, tipo:str):
        if tipo not in dict(self.contato_escolhas).keys():
            raise ValueError
        return True
    
    def set_tipo(self, tipo:str):
        if self.validar_tipo(tipo) is True:
            self.tipo = tipo
            self.save()

    def get_tipo(self):
        return self.tipo
    
    def validar_chave(self, chave: str):
        if not chave.strip():
            raise ValueError
        if self.tipo == "telefone" and not re.fullmatch(r'\d{8,15}', chave):
            raise ValueError
        if self.tipo == "email" and not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', chave):
            raise ValueError
        return True

    def set_chave(self, chave:str):
        if self.validar_chave(chave) is True:
            self.chave = chave
            self.save()

    def get_chave(self):
        return self.chave


class Municipio(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'


class Pessoa(models.Model):
    tipo_doc = models.CharField(max_length=50)
    doc_ident = models.CharField(max_length=50, primary_key=True)
    id_mun = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="pessoas")
    nome = models.CharField(max_length=255)
    dt_nac = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ddd = models.CharField(max_length=5, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    nacionalidade = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome
    
    

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'


class Endereco(models.Model):
    # Relationship fields
    pessoa = models.OneToOneField(
        Pessoa, 
        on_delete=models.CASCADE, 
        related_name="endereco"
    )
    municipio = models.ForeignKey(
        Municipio, 
        on_delete=models.CASCADE, 
        related_name='enderecos'
    )
    
    # Address fields
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=8)
    
    # Additional useful fields
    is_endereco_fiscal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.municipio.nome}"

    @property
    def endereco_formatado(self):
        parts = [self.logradouro]
        if self.numero:
            parts.append(f"nº {self.numero}")
        if self.complemento:
            parts.append(self.complemento)
        if self.bairro:
            parts.append(self.bairro)
        parts.append(self.municipio.nome)
        parts.append(f"CEP: {self.formatar_cep()}")
        return ", ".join(part for part in parts if part)

    def formatar_cep(self):
        if len(self.cep) == 8:
            return f"{self.cep[:5]}-{self.cep[5:]}"
        return self.cep

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cep']),
            models.Index(fields=['is_endereco_fiscal']),
             ]
    
class PessoaFisica(Pessoa):
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, unique=True, null=True, blank=True)
    affiliation_pai = models.CharField(max_length=255, null=True, blank=True)
    affiliaton_mae = models.CharField(max_length=255, null=True, blank=True)
    pis = models.CharField(max_length=11, unique=True, null=True, blank=True)

    CHOICE_GENDER = [(0, 'Não Informado'),(1, 'Masculino'),(2, 'Feminino'),(3, 'Outro'), ] #levar como opção
    genero = models.IntegerField(choices= CHOICE_GENDER, null=True, blank=True)


    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf}"
    
    def get_cpf(self):
        return self.cpf

    def set_cpf(self, cpf):
        self.cpf = cpf
        self.save()

    def get_rg(self):
        return self.rg

    def set_rg(self, rg):
        self.rg = rg
        self.save()  

    def get_name(self):
        return self.nome 

    def set_name(self, nome):
        self.nome = nome
        self.save()

    def get_gender(self):
        return self.genero

    def set_gender(self, genero):
        self.genero = genero
        self.save()

    def get_birthday(self):
        return self.dt_nac

    def set_birthday(self, dt_nac):
        self.dt_nac = dt_nac
        self.save()
    
    def get_affiliation(self):
        return {"pai": self.filiacao_pai, "mae": self.filiacao_mae}

    def set_affiliation(self, pai: str, mae: str):
        self.filiacao_pai = pai
        self.filiacao_mae = mae
        self.save()
    
    def get_nacionality(self):
        return self.nacionalidade
    
    def set_nacionality(self, nacionalidade):
        self.nacionalidade = nacionalidade
        self.save()

    def get_pis(self):
        return self.pis

    def set_pis(self, pis: str):
        self.pis = pis
        self.save()


class PessoaJuridica(Pessoa):
    cnpj = models.CharField(max_length=18, unique=True)
    fantasy_name = models.CharField(max_length=255)
    corporate_reason = models.CharField(max_length=255)
    bonds = models.ManyToManyField(Pessoa, related_name="vinculos_pj")
    partners = models.ManyToManyField(Pessoa, related_name="partners_pj")
    opening_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"CNPJ: {self.cnpj}, NOME: {self.fantasy_name}"
    
    def get_cnpj(self):
        return self.cnpj
    
    def get_fantasy_name(self):
        return self.fantasy_name
    
    def get_corporate_reason(self):
        return self.corporate_reason
    
    def get_bonds(self):
        return self.bonds
    
    def get_partners(self):
        return self.partners
    
    def get_opening_date (self):
        return self.opening_date 
    
    def get_closing_date(self):
        return self.closing_date
