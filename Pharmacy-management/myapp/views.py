from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import PharmacyManager,Medicine

# Create your views here.
def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == "POST":
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
                return render(request,'login.html',{'msg':msg})
            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})   
    else:
        return render(request,'signup.html')
	
def login(request):
    if request.method == "POST":
        try:
            manager = PharmacyManager.objects.get(email=request.POST['email'])
            if manager.password == request.POST['password']:
                request.session['fname'] = manager.fname
                request.session['lname'] = manager.lname
                request.session['email'] = manager.email
                request.session['pharmacyname'] = manager.pharmacyname
                request.session['number'] = manager.number
                msg = "Login successful"
                return render(request, 'index.html', {'msg': msg}) 
                msg = "Incorrect Password"
                return render(request, 'login.html', {'msg': msg})
        except PharmacyManager.DoesNotExist:
            msg = "Email Not Registered"
            return render(request, 'login.html', {'msg': msg})
    else:
        msg = "Please use the login form" 
        return render(request, 'login.html', {'msg': msg})

def logout(request):
    if 'email' in request.session:
        del request.session['lname']
        del request.session['fname']
        del request.session['email']
        del request.session['pharmacyname']
        del request.session['number']
        msg = "User Logged Out Successfully"
        return render(request,'index.html',{'msg':msg})
    else:
        msg = "Session Expired. Please Login Again."
    return render(request, 'login.html', {'msg': msg})

def add_medicine(request):
    return render(request,'add-medicine.html')

def medicines(request):
    if request.method == "POST": 
            manager=PharmacyManager.objects.get(email=request.session['email'])
            medicine_name = request.POST['medicine_name']
            medicine = Medicine.objects.create(
            manager=manager,
            medicine_name=request.POST['medicine_name'],
            price=request.POST['price'],
            company=request.POST['company'],
            use=request.POST['use'],
            quantity=request.POST['quantity'],
            )           
            msg = "Medicine added successfully!"
            return redirect('view-medicines')
    else:
        return render(request,'index.html')
  
def view_medicines(request):
   manager=PharmacyManager.objects.get(email=request.session['email'])
   medicines1=Medicine.objects.filter(manager=manager)
   return render(request,'view-medicines.html',{'medicines1':medicines1})

def delete(request, pk):
        medicine = Medicine.objects.get(pk=pk)
        medicine.delete()
        msg = "Product deleted successfully."
        return redirect('view-medicines')
        
def edit(request,pk):
    medicine = Medicine.objects.get(pk=pk)
    if request.method == "POST":
        medicine.price=request.POST['price']
        medicine.company=request.POST['company']
        medicine.use=request.POST['use']
        medicine.quantity=request.POST['quantity']
        medicine.save()
        msg = "Medicine Updated Successfully"
        return redirect('view-medicines')
    else:
        msg="medicine not updated"
        return render(request,'medicine-edit.html',{'medicine':medicine,'msg':msg})

        
