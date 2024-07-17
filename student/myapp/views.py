from django.shortcuts import render
from .models import Student

# Create your views here.
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == "POST":
        try:
            student=Student.object.get(email=request.POST['email'])
            msg="email already registered"
            return render(request,'index.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                Student.objects.create(
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        password=request.POST['password'],
                        address=request.POST['address'],
                        gender=request.POST['gender'],
                        qualification=request.POST['qualification']
                    )
                msg="user sign up sucessfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})   
    else:
        return render(request,'signup.html')
    
def login(request):
    if request.method == "POST":
        try:
            student = Student.objects.get(email=request.POST['email'])
            if student.password == request.POST['password']:
                request.session['fname'] = student.fname
                request.session['lname'] = student.lname
                request.session['email'] = student.email
                request.session['password']=student.password
                msg = "Login successful"
                return render(request, 'index.html', {'msg': msg}) 
                msg = "Incorrect Password"
                return render(request, 'login.html', {'msg': msg})
        except Student.DoesNotExist:
            msg = "Email Not Registered"
            return render(request, 'login.html', {'msg': msg})
    else:
        msg = "Please use the login form" 
        return render(request, 'login.html', {'msg': msg})