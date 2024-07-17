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
    
class Medicine(models.Model):
    manager=models.ForeignKey(PharmacyManager,on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for price
    company = models.CharField(max_length=255)
    use = models.TextField()
    quantity = models.IntegerField(default=0)
        
    def __str__(self):
        return f"{self.medicine_name} ({self.company})"

