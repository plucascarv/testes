from django.db import models

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

    def __str__(self):
        return self.nome

    def get_ID(self):
        return self.doc_ident

    def get_data_cadastro(self):
        return self.data_cadastro

    def get_nome(self):
        return self.nome

    def get_enderecos(self):
        return self.enderecos.all()

    def get_contatos(self):
        return self.contatos.all()

    def validar_endereco(self, endereco):
        
        if not endereco.logradouro or not endereco.numero or not endereco.bairro or not endereco.cep:
            return False
        
        if not re.match(r'^\d{5}-\d{3}$', endereco.cep):
            return False
        return True

    def validar_contato(self, contato):
      
            tipos_validos = ['email', 'telefone']
      
            if contato.tipo not in tipos_validos:
                return False

            if contato.tipo == 'email' and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contato.chave):
                return False
            if contato.tipo == 'telefone' and not re.match(r'^\+?\d{10,15}$', contato.chave):
                return False
            return True
    
    def add_contato(self, contato):
        if self.validar_contato(contato):
            self.contatos.add(contato)

    def add_endereco(self, endereco):
        if self.validar_endereco(endereco):
            self.enderecos.add(endereco)

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'


class Endereco(models.Model):
    # Relationship fields
    pessoa = models.ForeignKey(
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