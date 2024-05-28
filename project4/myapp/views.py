from django.shortcuts import render
from .models import Contact,User

#email send mate ni library che..down"..
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method=="POST":
		Contact.objects.create(
			name=request.POST['name'],
			email=request.POST['email'],
			mobile=request.POST['mobile'],
			remarks=request.POST['remarks']
			)
		msg="contact saved successfully!!"
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'msg':msg,'contact':contacts})
	else:
		contacts=Contact.objects.all().order_by("-id")[:3]
		return render(request,'contact.html',{'contacts':contacts})

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="email already registered"
			return render(request,"signup.html",{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
					fname=request.POST['fname'],
					lname=request.POST['lname'],
					email=request.POST['email'],
					password=request.POST['password'],
					mobile=request.POST['mobile'],
					address=request.POST['address']
				)
				msg="user signup sucessfully"
				return render(request,'signup.html',{'msg':msg})
			else:
				msg="password nd confirm password doesn't match"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				return render(request,'index.html')
			else:
				msg="incorrect password"
				return render(request,'login.html',{'msg':msg})
		except:
			msg="email not registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		msg="user logged out sucessfully"
		return render(request,'login.html',{'msg':msg})
	except:
		msg="user logged out sucessfully"
		return render(request,'login.html',{'msg':msg})

def change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				del request.session['email']
				del request.session['fname']
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
	
def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			#otp random mklva 
			otp=random.randint(1000,9999)
			subject = 'otp for forgot password'
			message = 'hello '+user.fname+', your otp for forgot-password is '+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
#upr ni line of code thi j te ni id pr otp send thase ..
#otp bni ne send thy jaay p66i bja url pr aavu joi atle bja function ma jvu jose..
#1 function no data bja ma use krva session create krvo jose jema otp 6
			request.session['otp']=otp
			request.session['email_otp']=user.email
			return render(request,'otp.html')		
		except Exception as e:
			print(e)
			msg="Email Not Registered"
			return render(request,'forgot-password.html',{'msg':msg})
	else:
		return render(request,'forgot-password.html')
	
def verify_otp(request):
	otp=int(request.POST['otp'])
	if otp==int(request.session['otp']):
		del request.session['otp']
		return render(request,'new-password.html')
	else:
		msg="invalid otp"
		return render(request,'otp.html',{'msg':msg})
	
def new_password(request):
	if request.POST['new_password']==request.POST['cnew_password']:
		user=User.objects.get(email=request.session['email_otp'])
		user.password=request.POST['new_password']
		user.save()
		del request.session['email_otp']
		msg="password updated sucessfully"
		return render(request,'login.html',{'msg':msg})
	else:
		msg="new password and confirm password does not matched"
		return render(request,'new-password.html',{'msg':msg})