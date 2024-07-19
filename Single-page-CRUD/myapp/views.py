from django.shortcuts import render,redirect
from .models import Student

# Create your views here.
# def index(request):
#     return render(request,'index.html')

def index(request):
    if request.method == 'POST':
        student=Student.objects.create(
            firstname=request.POST['firstname'],
			lastname=request.POST['lastname'],
			email=request.POST['email'],
			password=request.POST['password']
        )
        student = Student.objects.all()
        msg="student added sucessfull"        
        return render(request,'index.html',{'msg':msg,'student':student})
    else:
        student = Student.objects.all()
        return render(request,'index.html',{'student':student})

def delete(request,pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'GET':
        student.delete()
        return redirect('index')
    else:
        return render(request,'index.html',{'student':Student.objects.all()})

def edit(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "GET":
        student.firstname = request.POST['firstname']
        student.lastname = request.POST['lastname']
        student.email = request.POST['email']
        student.password = request.POST['password']
        student.save()
        return redirect('index')
    else:
        return render(request, 'index.html', {'student': student})

