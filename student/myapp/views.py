from django.shortcuts import render,redirect
from .models import Faculty,Student
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return render(request,'index.html')
    
def login(request):
    if request.method == "POST":
        try:
            faculty = Faculty.objects.get(femail=request.POST['femail'])
            if(faculty.fpassword == request.POST['fpassword']):
                request.session['femail'] = faculty.femail
                msg = "Login successful"
                return render(request, 'index.html', {'msg': msg})
            else:
                msg = "Invalid email or password"
                return render(request, 'login.html', {'msg': msg})
        except ObjectDoesNotExist: 
            msg = "Invalid email or password"
            return render(request, 'login.html', {'msg': msg})
    else:
        msg = "Please enter your login credentials."
        return render(request, 'login.html', {'msg': msg})
    
def logout(request):
    if 'femail' in request.session:
        del request.session['femail']
        msg="logout sucessfully"
        return render(request,'index.html',{'msg':msg})
    else:
        msg="session expire login again"
        return render(request,'index.html',{'msg':msg})

def add_student(request):
    return render(request,'add-student.html')

def add_to_student(request):
    if request.method == "POST":
            faculty=Faculty.objects.get(femail=request.session['femail'])
            email=request.POST['email']            
            student=Student.objects.create(
            faculty=faculty,
            fname=request.POST['fname'],
            lname=request.POST['lname'],
            email=request.POST['email'],
            password=request.POST['password'],
            gender=request.POST['gender'],
            qualification=request.POST['qualification'],
            address=request.POST['address'],
            )
            msg="student added sucessfully"
            return render(request,'view-student.html',{'msg':msg})
    else:
        return render(request,'index.html')
    
def view_student(request):
    faculty=Faculty.objects.get(femail=request.session['femail'])
    student=Student.objects.filter(faculty=faculty)
    return render(request,'view-student.html',{'student':student})

def delete(request, pk):
        student = Student.objects.get(pk=pk)
        student.delete()
        msg = "Product deleted successfully."
        return redirect('view-student')

def edit(request,pk):
    student=Student.objects.get(pk=pk)
    return render(request,'edit-student.html',{'student':student})

def edit_student(request,pk):
    student = Student.objects.get(pk=pk)
    if request.method == "POST":
        student.fname=request.POST['fname']
        student.lname=request.POST['lname']
        student.address=request.POST['address']
        student.qualification=request.POST['qualification']
        student.save()
        msg = "student Updated Successfully"
        return redirect('view-student')
    else:
        msg="student not updated"
        return render(request,'edit-student.html',{'student':student,'msg':msg})

