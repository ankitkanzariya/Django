from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class Customer(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.PositiveBigIntegerField()
    address=models.TextField()
    password = models.CharField(max_length=128, default='123')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    

    def __str__(self):
        return self.fname+" "+self.lname

class Policy(models.Model):
    category = models.ForeignKey
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} (Premium: {self.premium:,.2f})"
    
class LifeInsurancePolicy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.ImageField(upload_to='policy_pictures', blank=True)

    def __str__(self):
        return self.title