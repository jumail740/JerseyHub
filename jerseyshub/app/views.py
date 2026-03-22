from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .models import Profile
from .models import Jersey,Wishlist,Cart,Order
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
        return redirect('login')
    
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
    cart_count = Cart.objects.filter(user=request.user).count()
    for jersey in new_arrivals:
        jersey.total_stock = sum(size.stock for size in jersey.sizes.all())

    for jersey in worldcup_jerseys:
        jersey.total_stock = sum(size.stock for size in jersey.sizes.all())

    for jersey in club_jerseys:
        jersey.total_stock = sum(size.stock for size in jersey.sizes.all())

    context = {
        "new_arrivals": new_arrivals,
        "worldcup_jerseys": worldcup_jerseys,
        "club_jerseys":club_jerseys,
        "whislist_jerseys":whislist_jerseys,
        'wishlist_count':wishlist_count,
        "cart_count": cart_count
    }
    return render(request,'homepage.html',context)


@login_required
def jersey_detail(request, id):

    jersey = get_object_or_404(Jersey, id=id)

    wishlist_jerseys = Wishlist.objects.filter(
        user=request.user
    ).values_list('jersey_id', flat=True)

    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    size_list = ["S", "M", "L", "XL"]
    sizes = {}

    for s in size_list:
        obj = jersey.sizes.filter(size=s).first()
        sizes[s] = obj.stock if obj else 0
    
    total_stock=sum(sizes.values())

    context = {
        'jersey': jersey,
        'wishlist_jerseys': wishlist_jerseys,
        'wishlist_count': wishlist_count,
        'sizes': sizes,
        'total_stock': total_stock
    }

    return render(request, 'jersey_detail.html', context)


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
    
    for j in jersey:
        j.total_stock = sum(size.stock for size in j.sizes.all())

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
    for j in jerseys:
        j.total_stock = sum(size.stock for size in j.sizes.all())
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
    for j in jerseys:
        j.total_stock = sum(size.stock for size in j.sizes.all())
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

    wishlist_items = Wishlist.objects.filter(user=req.user)

    for j in wishlist_items:
        j.jersey.total_stock = sum(size.stock for size in j.jersey.sizes.all())

    return render(req, 'wishlist.html', {'wishlist_items': wishlist_items})

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
    size = request.POST.get("size")
    player_name = request.POST.get("player_name")
    player_number = request.POST.get("player_number")
    
    if player_number == "":
       player_number = None

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        jersey=jersey,
         size=size,
        player_name=player_name,
        player_number=player_number,
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')



@login_required
def cart_page(req):
    cart_items=Cart.objects.filter(user=req.user)
    total = sum(item.total_price() for item in cart_items)
    related_jerseys = []
    for item in cart_items:
        related = Jersey.objects.filter(team=item.jersey.team).exclude(id=item.jersey.id)[:4]
        related_jerseys.extend(related)
    related_jerseys = list({j.id: j for j in related_jerseys}.values())
    
    return render(req,'cart.html',{'cart_items':cart_items,"total":total,'related_jerseys': related_jerseys})


@login_required
def remove_from_cart(request, cart_id):
    item = Cart.objects.filter(id=cart_id, user=request.user).first()

    if item:
        item.delete()

    return redirect('cart_page')

@login_required
def inc_quantity(req,cart_id):
    cart_item= Cart.objects.get(id=cart_id)
    
    cart_item.quantity +=1
    cart_item.save()
    return redirect('cart_page')

@login_required
def dec_quantity(req,cart_id):
    cart_item= Cart.objects.get(id=cart_id)
    
    if cart_item.quantity > 1:
       cart_item.quantity -=1
       cart_item.save()
    return redirect('cart_page')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order

@login_required
def buy_now(request):

    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.jersey.price * item.quantity

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment = request.POST.get("payment")
        
        if payment == "upi":
            return render(request, "upi_payment.html", {
                "cart_items": cart_items,
                "total_price": total_price,
                 "fullname": fullname,   
                "email": email,    
                "address": address,
                "phone": phone
            })
        elif payment == "cod":
        
         for item in cart_items:

            item_total = item.jersey.price * item.quantity

            Order.objects.create(
                user=request.user,
                jersey=item.jersey,
                player_name=item.player_name,
                player_number=item.player_number,
                quantity=item.quantity,
                total_price=item_total,
                address=address,
                phone=phone,
                payment_method="Cash on Delivery"
            )

        cart_items.delete()

        return redirect("order_success")

    return render(request, "checkout.html", {"cart_items": cart_items,"total_price": total_price})

def order_success(request):
    return render(request, "order_success.html")


@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "my_orders.html", {"orders": orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ['Pending', 'Shipped']:
        order.status = 'Cancelled'
        order.save()

    return redirect('my_orders')

@login_required
def confirm_upi(request):

    cart_items = Cart.objects.filter(user=request.user)

    if request.method == "POST":

        address = request.POST.get("address")
        phone = request.POST.get("phone")

        for item in cart_items:

            item_total = item.jersey.price * item.quantity

            Order.objects.create(
                user=request.user,
                jersey=item.jersey,
                player_name=item.player_name,
                player_number=item.player_number,
                quantity=item.quantity,
                total_price=item_total,
                address=address,
                phone=phone,
                payment_method="UPI",
                payment_status="Paid"
            )

        cart_items.delete()

        return redirect("order_success") 



from datetime import timedelta,date
@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    order.delivery_date = date.today() + timedelta(days=5)
    expected_delivery = order.created_at + timedelta(days=5)

    return render(request, "order_detail.html", {
        "order": order,
        "expected_delivery": expected_delivery
    })
    
def upi_payment(request):
    return render(request, "upi_payment.html", {
        "fullname": request.POST.get("fullname"),
        "email": request.POST.get("email"),
        "phone": request.POST.get("phone"),
        "address": request.POST.get("address"),
        "total_price": request.POST.get("total_price"),
    })