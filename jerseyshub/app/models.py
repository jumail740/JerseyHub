from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    
    def __str__(self):
        return self.user.username
    
    
class Jersey(models.Model):
    CATEGORY = (
        ('club','Club Jersey'),
        ('worldcup','World Cup Jersey'),
    )

    name=models.TextField()
    team=models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='jerseys/')
    img2 = models.ImageField(upload_to='jerseys/')
    img3 = models.ImageField(upload_to='jersey/', null=True, blank=True)
    img4= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    img5= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    img6= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    img7= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    img8= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    img9= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    img10= models.ImageField(upload_to='jerseys/',null=True, blank=True)
    stock= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    players = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    jersey=models.ForeignKey(Jersey,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.jersey.name}"
    
class Cart(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    jersey=models.ForeignKey(Jersey,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    
    def total_price(self):
        return self.jersey.price * self.quantity
    