from django.contrib import admin
from .models import Certificate_Owners, Certificate_Tokens, Certificates

# Register your models here.
admin.site.register(Certificate_Owners)
admin.site.register(Certificates)
admin.site.register(Certificate_Tokens)
