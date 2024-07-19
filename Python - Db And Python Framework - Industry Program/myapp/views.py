from django.shortcuts import render,redirect
from .models import User,InsuranceApplication,Question,PolicyHolder

# Create your views here.
def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				request.session['email']=user.email
				return render(request,'index.html')
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
	 	msg='user logout sucessfull'
	 	return render(request,'login.html',{'msg':msg})
	except:
		msg='user logout sucessfull'
		return render(request,'login.html',{'msg':msg})

def forget(request):
	return render(request,'forget.html')

def index(request):
	return render(request,'index.html')

def register(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg="Email Already Registered"
			return render(request,'login.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						username=request.POST['username'],
						mobile=request.POST['mobile'],
						password=request.POST['password'],
					)
				msg="User Sign Up Successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not Matched"
				return render(request,'register.html',{'msg':msg})
	else:
		return render(request,'register.html')



def adminpanel(request):
    # Get counts from your models
    total_users = User.objects.count()
    total_questions = Question.objects.count()
    total_applied_policy_holders = InsuranceApplication.objects.count()
    # approved_policy_holders = PolicyHolder.objects.filter(status='approved').count()
    # disapproved_policies = PolicyHolder.objects.filter(status='disapproved').count()
    # waiting_for_approval = PolicyHolder.objects.filter(status='pending').count()

    context = {
        'total_users': total_users,
        'total_questions': total_questions,
        'total_applied_policy_holders': total_applied_policy_holders,
        # 'approved_policy_holders': approved_policy_holders,
        # 'disapproved_policies': disapproved_policies,
        # 'waiting_for_approval': total_applied_policy_holders,
    }
    return render(request, 'admin.html', context)

def insurance_application(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        insurance_type = request.POST.get('insurance_type')

        InsuranceApplication.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            dob=dob,
            gender=gender,
            insurance_type=insurance_type
        )

        return redirect('insurance_application')

    else:
        return render(request, 'insurance_application.html')



# @login_required
def submit_question(request):
   if request.method == 'POST':
        question_text = request.POST.get('question')
        
        if question_text:
            user_email = request.session.get('email')
            
            if user_email:
                user = User.objects.get(email=user_email)
                Question.objects.create(
                    question_text=question_text,
                    user=user
                )
                return redirect('submit_question')  
            else:
                return render(request, 'submit_question.html', {'error': 'User not logged in'})
        else:
            return render(request, 'submit_question.html', {'error': 'Question cannot be empty'})
   else:
        return render(request, 'submit_question.html')

def PolicyHolder(request):
    user_email = request.session.get('email')
    if not user_email:
        return HttpResponse("User email not found in session!")

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return HttpResponse("User not found!")

    policy_holders = PolicyHolder.objects.filter(user=user)

    context = {
        'policy_holders': policy_holders,
    }

    return render(request, 'admin.html', context)