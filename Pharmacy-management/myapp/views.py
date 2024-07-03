from django.shortcuts import render
# from django.contrib.auth import authenticate, login
from .models import PharmacyManager

# Create your views here.
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method=='POST':
        try:
            manager=PharmacyManager.object.get(email=request.POST['email'])
            msg="email already registered"
            return render(request,'index.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                PharmacyManager.objects.create(
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        password=request.POST['password'],
                        pharmacyname=request.POST['pharmacyname'],
                        number=request.POST['number'],
                    )
                msg="user sign up sucessfully"
                return render(request,'index.html',{'msg':msg})
            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})   
    else:
        return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			manager=PharmacyManager.objects.get(email=request.POST['email'])
			if manager.password==request.POST['password']:
				request.session['email']=manager.email
				request.session['fname']=manager.fname				
			else:
				msg="Incorrect Password"
				return render(request,'index.html',{'msg':msg})
		except Exception as e:
			print(e)
			msg="Email Not Registered"
			return render(request,'index.html',{'msg':msg})
	else:
            msg="else-part"
            return render(request,"index.html",{'msg':msg})
        