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
    path('home/',views.home),
    path('',views.login_view),
    path('logout/',views.logout_view),
    path('jersey/<int:id>/',views.jersey_detail,name='jersey_detail'),
    path('products/',views.products),
    path('club/', views.club_jerseys, name='club'),
    path('worldcup/', views.worldcup_jerseys, name='worldcup'),
    path('wishlist/<int:jersey_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/',views.wishlist_page,name='wishlist_page'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
