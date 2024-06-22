from django.contrib import admin
from .models import User
from .models import Product
from .models import Wishlist

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Wishlist)