from django.contrib import admin
from .models import Korisnici,Predmeti,Upisi

# Register your models here.

admin.site.register(Korisnici)
admin.site.register(Predmeti)
admin.site.register(Upisi)