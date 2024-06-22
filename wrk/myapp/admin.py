from django.contrib import admin
from .models import Customer
from .models import Policy
from .models import LifeInsurancePolicy

# Register your models here.
admin.site.register(Customer)
admin.site.register(Policy)
admin.site.register(LifeInsurancePolicy)
