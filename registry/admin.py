from django.contrib import admin
from .models import Municipio, Pessoa, Endereco

admin.site.register(Municipio)
admin.site.register(Pessoa)
admin.site.register(Endereco)