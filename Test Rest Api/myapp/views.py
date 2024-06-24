from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    if request.method == "POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        course=request.POST['course']
        print(course)
        url = "http://localhost:8000/api/students"
        querystring = {"fname":fname,"lname":lname,"email":email,"password":password,"course":course}
        response = requests.post(url, json=querystring)
        print(response)
        msg = "DATA inserted sucessfully.."
        return render(request,'index.html',{'msg':msg})
    else:
        return render(request,'index.html')