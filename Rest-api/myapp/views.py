from django.shortcuts import render
from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer

# Create your views here.
class StudentList(generics.ListCreateAPIView):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Student
    serializer_class=StudentSerializer