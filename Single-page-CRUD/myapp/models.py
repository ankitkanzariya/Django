from django.db import models

# Create your models here.
class Student(models.Model):
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.PositiveIntegerField(max_length=10)

    def __str__(self):
        return self.firstname +"-"+ self.lastname