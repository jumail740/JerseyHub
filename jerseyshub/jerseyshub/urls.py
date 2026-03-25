"""
URL configuration for jerseyshub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('home/',views.home,name='home'),
    path('',views.login_view),
    path('logout/',views.logout_view),
    path('jersey/<int:id>/',views.jersey_detail,name='jersey_detail'),
    path('products/',views.products,name='products'),
    path('club/', views.club_jerseys, name='club'),
    path('worldcup/', views.worldcup_jerseys, name='worldcup'),
    path('wishlist/<int:jersey_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/',views.wishlist_page,name='wishlist_page'),
    path('remove_wishlist/<int:jersey_id>/', views.remove_from_wishlist, name='remove_wishlist'),
    path('add_to_cart/<int:jersey_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
     path('remove_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:cart_id>/', views.inc_quantity, name='increase_quantity'),
path('decrease/<int:cart_id>/', views.dec_quantity, name='decrease_quantity'),
path("buy-now/", views.buy_now, name="buy_now"),
path('order-success/', views.order_success, name='order_success'),
path("my-orders/", views.my_orders, name="my_orders"),
path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
path('order/<int:id>/', views.order_detail, name='order_detail'),
 path('payment-success/', views.payment_success, name='payment_success'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
