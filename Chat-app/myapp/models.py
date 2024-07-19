from django.db import models

# Create your models here.
class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.PositiveIntegerField()
    profile_picture=models.ImageField(upload_to="profile_picture/")
    password=models.CharField(max_length=100)

    def __str__ (self):
        return self.fname +"-"+ self.lname