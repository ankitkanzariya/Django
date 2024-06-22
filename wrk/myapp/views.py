from django.shortcuts import render
import random

from .models import Customer
from .models import LifeInsurancePolicy

# Create your views here.
def index(request):
	return render(request,'index.html')

def policy(request):
    policies = LifeInsurancePolicy.objects.all()
    context = {'policies': policies}
    return render(request, 'policy.html')

def signup(request):
	if request.method=="POST":
		try:
			Customer.objects.get(email=request.POST['email'])
			msg="email already registered"
			return render(request,"signup.html",{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				Customer.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					password=request.POST['password'],
					mobile=request.POST['mobile'],
					address=request.POST['address'],
					profile_picture=request.FILES['profile_picture']
				)
				msg="Customer signup sucessfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="password nd confirm password doesn't match"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')
	
def login(request):
	if request.method=="POST":
		try:
			customer=Customer.objects.get(email=request.POST['email'])
			if customer.password==request.POST['password']:
				request.session['email']=customer.email
				request.session['fname']=customer.fname
				request.session['profile_picture']=customer.profile_picture.url
				return render(request,'index.html')
			else:
				msg="incorrect password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="email not registered"
			return render(request,'login.html',{'msg':msg})
	else:
		msg="customer logged-in sucessfully"
		return render(request,'login.html',{'msg':msg})
	
def change_password(request):
	if request.method=='POST':
		customer=Customer.objects.get(email=request.session['email'])
		if customer.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				customer.password=request.POST['new_password']
				customer.save()
				del request.session['email']
				del request.session['fname']
				del request.session['profile_picture']
				msg="password change sucessfully.."
				return render(request,'login.html',{'msg':msg})
			else:
				msg="new password and confirm password does not match"
				return render(request,'change-password.html',{'msg':msg})
		else:
				msg="old password does not match"
				return render(request,'change-password.html',{'msg':msg})
	else:
		return render(request,'change-password.html')

def logout(request):
    if request.session.get('email', False):
        del request.session['email']
        del request.session['fname']
        del request.session['profile_picture']
        msg = "You have been logged out successfully."
        return render(request, 'login.html', {'msg': msg})

    else:
        msg = "You were not logged in."
        return render(request, 'login.html', {'msg': msg})
