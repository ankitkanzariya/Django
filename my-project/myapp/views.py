from django.shortcuts import render,redirect

from .models import User
from .models import Product
from .models import Wishlist

#api ni madad thi otp send krva library..
import requests
import random

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def signup(request):
    if request.method=='POST':
        try:
            user=User.object.get(email=request.POST['email'])
            msg="email already registered"
            return render(request,'login.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                        usertype=request.POST['usertype'],
                        fname=request.POST['fname'],
                        lname=request.POST['lname'],
                        email=request.POST['email'],
                        password=request.POST['password'],
                        mobile=request.POST['mobile'],
                        address=request.POST['address'],
                        profile_picture=request.FILES['profile_picture'],
                    )
                msg="user sign up sucessfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="password and confirm password does not match"
                return render(request,'signup.html',{'msg':msg})   
    else:
        return render(request,'signup.html')
             
def login(request):
    if request.method=='POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                request.session['profile_picture']=user.profile_picture.url
                if user.usertype=="Buyer":
                    return render(request,'index.html')
                else:
                    return render(request,'seller-index.html')
            else:
               msg="incorrect password" 
               return render(request,'login.html',{'msg':msg})
        except:
            msg="email not registered"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def product(request):
	products=Product.objects.all()
	return render(request,'product.html',{'products':products})

def blog_list(request):
    return render(request,'blog_list.html')

def testimonial(request):
    return render(request,'testimonial.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_picture']
        msg="user logout sucessfully..."
        return render(request,'login.html',{'msg':msg})
    except:
        msg="user loggedout sucessfully"
        return render(request,'login.html',{'msg':msg})
    
def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=="POST":
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_picture=request.FILES['profile_picture']
		except:
			pass
		user.save()
		msg="Profile Updated Successfully"
		request.session['profile_picture']=user.profile_picture.url
		if user.usertype=="Buyer":
			return render(request,'profile.html',{'user':user,'msg':msg})
		else:
			return render(request,'seller-profile.html',{'user':user,'msg':msg})
	else:
		if user.usertype=="Buyer":
			return render(request,'profile.html',{'user':user})
		else:
			return render(request,'seller-profile.html',{'user':user})
    
def change_password(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                user.password=request.POST['new_password']
                user.save()
                msg="Password changed sucessfully"
                del request.session['email']
                del request.session['fname']
                del request.session['profile_picture']
                return render(request,'login.html',{'msg':msg})
            else:
                msg="New-password and Confirm new password doesn't matched"
                return render(request,'change-password.html',{'msg':msg})
        else:
             msg="old password doesn't matched"
             return render(request,'change-password.html',{'msg':msg})
    else:
        return render(request,'change-password.html')

def forgot_password(request):
    if request.method=="POST":
        try:
            user=User.objects.get(mobile=request.POST['mobile'])
            mobile=request.POST['mobile']
            otp=str(random.randint(1000,9999))
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {"authorization":"OgMy8vpKc1ZFi095PtbemLjT3kuhzrwAaBoQE6RSs2UIJqWYx4EhYUiL3VI15AmOJkCd8r0tQMecnWgD","sender_id":"DLT_SENDER_ID","message":"YOUR_MESSAGE_ID","variables_values":"otp","route":"otp","numbers":mobile}
            headers = {'cache-control': "no-cache"}
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            request.session['otp']=otp
            request.session['mobile']=mobile
            return render(request,'otp.html')
        except:
            msg="mobile not registered"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')

def verify_otp(request):
    if int(request.POST['otp1'])==int(request.session['otp']):
        del request.session['otp']
        return render(request,'new-password.html')
    else:
        msg="invalid otp"
        return render(request,'otp.html',{'msg':msg})
    
def update_password(request):
    if request.POST['new_password']==request.POST['cnew_password']:
        user=User.objects.get(mobile=request.session['mobile'])
        user.password=request.POST['new_password']
        user.save()
        msg="password updated sucessfully.."
        del request.session['mobile']
        return render(request,'login.html',{msg:msg})
    else:
        msg="New password and confirm password doesn't matched"
        return render(request,'new-password.html',{'msg':msg})
    
def add_product(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        Product.objects.create(
            seller=seller,
            product_catagory=request.POST['product_catagory'],
            product_sub_catagory=request.POST['product_sub_catagory'],
            product_name=request.POST['product_name'],
            product_desc=request.POST['product_desc'],
            product_price=request.POST['product_price'],
            product_image=request.FILES['product_image']
        )
        msg="product added sucessfully"
        return render(request,'seller-add-product.html',{'msg':msg})
    else:
        return render(request,'seller-add-product.html')
    
def view_product(request):
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)
    return render(request,'seller-view-product.html',{'products':products})

def seller_product_details(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'seller-product-details.html',{'product':product})

def product_details(request,pk):
    wishlist_flag=False
    user=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    try:
        Wishlist.objects.get(user=user,product=product)
        wishlist_flag=True
    except:
        pass
    return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag})


def seller_product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        product.product_catagory=request.POST['product_catagory']
        product.product_sub_catagory = request.POST['product_sub_catagory']
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_pr ice']
        product.product_desc = request.POST['product_desc']

        try:
            product.product_image = request.FILES['product_image']
        except KeyError:
            pass
        product.save()
        msg = "Product Updated Successfully"
        return render(request, 'seller-product-edit.html', {'product': product, 'msg': msg})

    else:
        # No need to refetch product in GET request, it's already retrieved at the beginning
        return render(request, 'seller-product-edit.html', {'product': product})


def seller_product_delete(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    msg='product deleted sucessfully!!!'
    return redirect('view-product')

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(product=product,user=user)
	#msg="Product added to wishlist"
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.filter(user=user)
	return render(request,'wishlist.html',{'wishlists':wishlist})
