from django.contrib import admin
from .models import Municipality, Person, Address
admin.site.register(Municipality)
admin.site.register(Person)
admin.site.register(Address)