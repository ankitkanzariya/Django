from django.db import models

# Create your models here.
class PharmacyManager(models.Model):
    fname = models.CharField(max_length=50) 
    lname = models.CharField(max_length=50) 
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128) 
    pharmacyname = models.CharField(max_length=255) 
    number = models.CharField(max_length=10) 

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.pharmacyname})"

