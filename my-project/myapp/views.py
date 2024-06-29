from django.shortcuts import render,redirect
from .models import User
from .models import Product
from .models import Wishlist
from .models import Cart
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
import json
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://localhost:8000'

#api ni madad thi otp send krva library..
import requests
import random


def index(request):
	products=Product.objects.all()[:4]
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="Buyer":
			return render(request,'index.html',{'products':products})
		else:
			return render(request,'seller-index.html')
	except:
		return render(request,'index.html',{'products':products})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def product(request):
	products=Product.objects.all()
	return render(request,'product.html',{'products':products})

def blog_list(request):
	return render(request,'blog_list.html')

def testimonial(request):
	return render(request,'testimonial.html')

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
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_picture']=user.profile_picture.url
				wishlists=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlists)
				carts=Cart.objects.filter(user=user)
				request.session['cart_count']=len(carts)
				if user.usertype=="Buyer":
					return render(request,'index.html')
				else:
					return render(request,'seller-index.html')
			else:
				msg="Incorrect Password"
				return render(request,'login.html',{'msg':msg})
		except Exception as e:
			print(e)
			msg="Email Not Registered"
			return render(request,'login.html',{'msg':msg})
	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_picture']
		del request.session['wishlist_count']
		del request.session['cart_count']
		msg="User Logged Out Successfully"
		return render(request,'login.html',{'msg':msg})
	except:
		msg="User Logged Out Successfully"
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
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				msg="Password Changed Successfully"
				del request.session['email']
				del request.session['fname']
				del request.session['profile_picture']
				return render(request,'login.html',{'msg':msg})
			else:
				msg="New Password & Confirm New Password Does Not Matched"
				if user.usertype=="Buyer":
					return render(request,'change_password.html',{'msg':msg})
				else:
					return render(request,'seller-change_password.html',{'msg':msg})
		else:
			msg="Old Password Does Not Matched" 
			if user.usertype=="Buyer":
				return render(request,'change_password.html',{'msg':msg})
			else:
				return render(request,'seller-change_password.html',{'msg':msg})			
	else:
		if user.usertype=="Buyer":			
			return render(request,'change_password.html')
		else:
			return render(request,'seller-change_password.html')

def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(mobile=request.POST['mobile'])
			mobile=request.POST['mobile']
			otp=str(random.randint(1000,9999))
			request.session['otp']=otp
			request.session['mobile']=mobile
			return render(request,'otp.html')					
		except:
			msg="Mobile Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})
	else:
		return render(request,'forgot_password.html')

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
	cart_flag=False
	user=User()
	try:	
		user=User.objects.get(email=request.session['email'])
	except:
		pass
	product=Product.objects.get(pk=pk)
	try:
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass

	try:
		Cart.objects.get(user=user,product=product)
		cart_flag=True
	except:
		pass
	return render(request,'product-details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})

def seller_product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        product.product_catagory=request.POST['product_catagory']
        product.product_sub_catagory = request.POST['product_sub_catagory']
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_price']
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
	#msg="Product Added To Wishlist"
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlists=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlists)
	return render(request,'wishlist.html',{'wishlists':wishlists})

def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(user=user,product=product)
	wishlist.delete()
	return redirect('wishlist')

def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(
		product=product,
		user=user,
		product_price=product.product_price,
		product_qty=1,
		total_price=product.product_price
	)
	# msg="Product Added To Wishlist"
	return redirect('cart')

def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user)
	for i in carts:
		net_price=net_price+i.total_price
	request.session['cart_count']=len(carts)
	return render(request,'cart.html',{'carts':carts,'net_price':net_price})

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(user=user,product=product)
	cart.delete()
	return redirect('cart')

def change_qty(request,pk):
	cart=Cart.objects.get(pk=pk)
	product_qty=int(request.POST['product_qty'])
	cart.product_qty=product_qty
	cart.total_price=product_qty*cart.product_price
	cart.save()
	return redirect('cart')

@csrf_exempt
def create_checkout_session(request):
	amount = int(json.load(request)['post_data'])
	final_amount=amount*100
	
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'inr',
				'product_data': {
					'name': 'Checkout Session Data',
					},
				'unit_amount': final_amount,
				},
			'quantity': 1,
			}],
		mode='payment',
		success_url=YOUR_DOMAIN + '/success.html',
		cancel_url=YOUR_DOMAIN + '/cancel.html',)
	return JsonResponse({'id': session.id})

def success(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=False)
	for i in carts:
		i.payment_status=True
		i.save()
	carts=Cart.objects.filter(user=user,payment_status=False)
	request.session['cart_count']=len(carts)
	return render(request,'success.html')

def cancel(request):
	return render(request,'cancel.html')

def myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'myorder.html',{'carts':carts})

def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)

def seller_myorder(request):
	user=User.objects.get(email=request.session['email'])
	carts=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'myorder.html',{'carts':carts})