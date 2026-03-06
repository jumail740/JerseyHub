from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import Profile
from .models import Jersey


# Create your views here.

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password!=confirm_password:
            messages.error(request,'Password do not match')
            return redirect(register)
        
        if User.objects.filter(username = username).exists():
            messages.error(request,'Username already exists')
            return redirect(register)
        user=User.objects.create_user(
        username=username,
        email=email,
        password=password
       )     
        Profile.objects.create(user=user,phone=phone)
        messages.error(request,'Registration Successfull')
        return redirect(login)
    
    return render(request,'register.html')

def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect(home)
        else:
            messages.error(request,'invalid username or password')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect(login_view)

def home(request):
    new_arrivals = Jersey.objects.all().order_by('-created_at')[:8]
    worldcup_jerseys = Jersey.objects.filter(category='worldcup')[:8]
    club_jerseys= Jersey.objects.filter(category='club')[:8]

    context = {
        "new_arrivals": new_arrivals,
        "worldcup_jerseys": worldcup_jerseys,
        "club_jerseys":club_jerseys
    }
    return render(request,'homepage.html',context)

def jersey_detail(request,id):
    jersey= get_object_or_404(Jersey,id=id)
    return render(request,'jersey_detail.html',{'jersey':jersey})

def products(request):
    jersey=Jersey.objects.all()
    return render(request,'products.html',{'jersey':jersey})

def club_jerseys(request):
    jerseys = Jersey.objects.filter(category='club')
    return render(request,'club.html',{'jerseys': jerseys})

def worldcup_jerseys(request):
    jerseys = Jersey.objects.filter(category='worldcup')
    return render(request,'worldcup.html',{'jerseys': jerseys})