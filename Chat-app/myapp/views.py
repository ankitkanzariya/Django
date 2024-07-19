from django.shortcuts import render
from .models import User

# Create your views here.
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="email already registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    profile_picture=request.FILES['profile_picture'],
                    password=request.POST['password'],
                    mobile=request.POST['mobile']                   
                )
                msg="user signup sucessfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')