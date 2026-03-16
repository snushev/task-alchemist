from django.contrib import admin
from .models import Vault, Secret

# Register your models here.

admin.site.register(Vault)
admin.site.register(Secret)
