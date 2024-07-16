from django.contrib import admin
from .models import PharmacyManager,Medicine

# Register your models here.
admin.site.register(PharmacyManager)
admin.site.register(Medicine)
