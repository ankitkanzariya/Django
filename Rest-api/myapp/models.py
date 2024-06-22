from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store securely using a hasher
    course = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fname} {self.lname}"

