from django.contrib import admin
from .models import User,InsuranceApplication,Question,PolicyHolder
# Register your models here.

admin.site.register(User)
admin.site.register(InsuranceApplication)
admin.site.register(Question)
admin.site.register(PolicyHolder)
