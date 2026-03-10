from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import Profile
from .models import Jersey,Wishlist,Cart
from django.db.models import Q


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
            return redirect('register')
    return render(request,'login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect(login_view)



@login_required
def home(request):
    new_arrivals = Jersey.objects.all().order_by('-created_at')[:8]
    worldcup_jerseys = Jersey.objects.filter(category='worldcup')[:8]
    club_jerseys= Jersey.objects.filter(category='club')[:8]
    
    whislist_jerseys= Wishlist.objects.filter(
        user=request.user
    ).values_list('jersey_id',flat=True)
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        "new_arrivals": new_arrivals,
        "worldcup_jerseys": worldcup_jerseys,
        "club_jerseys":club_jerseys,
        "whislist_jerseys":whislist_jerseys,
        'wishlist_count':wishlist_count,
    }
    return render(request,'homepage.html',context)


@login_required
def jersey_detail(request,id):
    jersey= get_object_or_404(Jersey,id=id)
    whislist_jerseys= Wishlist.objects.filter(
        user=request.user
    ).values_list('jersey_id',flat=True)
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    context = {
        'jersey': jersey,
        'whislist_jerseys': whislist_jerseys,
        'wishlist_count': wishlist_count
    }
    
    return render(request,'jersey_detail.html',context)


@login_required
def products(request):
    search = request.GET.get('search')

    jersey = Jersey.objects.all()

    if search:
        jersey = jersey.filter(
            Q(team__icontains=search) |
            Q(players__icontains=search)|
            Q(category__icontains=search)
        )

    whislist_jerseys= Wishlist.objects.filter(
        user=request.user
    ).values_list('jersey_id',flat=True)
    wishlist_count= Wishlist.objects.filter(user=request.user).count()
    context = {
        'jersey': jersey,
        'whislist_jerseys': whislist_jerseys,
        'wishlist_count': wishlist_count
    }
    return render(request,'products.html',context)


@login_required
def club_jerseys(request):
    jerseys = Jersey.objects.filter(category='club')
    whislist_jerseys= Wishlist.objects.filter(
        user=request.user
    ).values_list('jersey_id',flat=True)
    wishlist_count= Wishlist.objects.filter(user=request.user).count()
    context = {
        'jerseys': jerseys,
        'whislist_jerseys': whislist_jerseys,
        'wishlist_count': wishlist_count
    }
    
    return render(request,'club.html',context)


@login_required
def worldcup_jerseys(request):
    jerseys = Jersey.objects.filter(category='worldcup')
    whislist_jerseys= Wishlist.objects.filter(
        user=request.user
    ).values_list('jersey_id',flat=True)
    wishlist_count= Wishlist.objects.filter(user=request.user).count()
    context = {
        'jerseys': jerseys,
        'whislist_jerseys': whislist_jerseys,
        'wishlist_count': wishlist_count
    }
    return render(request,'worldcup.html',context)


@login_required
def add_to_wishlist(req,jersey_id):
    jersey=Jersey.objects.get(id=jersey_id)
    
    Wishlist.objects.get_or_create(
        user=req.user,
        jersey=jersey
    )
    return redirect(req.META.get('HTTP_REFERER'))


def wishlist_page(req):
    wishlist_items =Wishlist.objects.filter(user=req.user)
    return render(req,'wishlist.html',{'wishlist_items':wishlist_items})

@login_required
def remove_from_wishlist(request, jersey_id):

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        jersey_id=jersey_id
    )

    wishlist_item.delete()

    return redirect('wishlist_page')

@login_required
def add_to_cart(request, jersey_id):

    jersey = get_object_or_404(Jersey, id=jersey_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        jersey=jersey
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')



@login_required
def cart_page(req):
    cart_items=Cart.objects.filter(user=req.user)
    total=0
    for item in cart_items:
        total += item.total_price()
    
    return render(req,'cart.html',{'cart_items':cart_items,"total":total})


@login_required
def remove_from_cart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    
    return redirect('cart_page')