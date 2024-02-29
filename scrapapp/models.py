from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Scrap(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_scraps')
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    condition=models.CharField(max_length=100)
    picture=models.ImageField(upload_to='scrapimages',null=True,blank=True)
    place=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ('Buy now','Buy now'),
        ('Sold out','Sold out')
    )
    status=models.CharField(max_length=100,choices=options,default='Buy now')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categories')
    
    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=100)
    profile_pic=models.ImageField(upload_to='profilepics',null=True,blank=True)
    wishlists = models.ManyToManyField(Scrap, related_name='wishlisted_by', blank=True)

    def __str__(self):
        return self.user.username

def create_profile(sender,created,instance,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('profile object created')
post_save.connect(create_profile,sender=User)


class Bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_bid')
    scrap=models.ForeignKey(Scrap,on_delete=models.CASCADE,related_name='scrap_bids')
    amount=models.PositiveIntegerField()
    options=(
        ('pending','pending'),
        ('accept','accept'),
        ('rejected','rejected')
    )
    status=models.CharField(max_length=100,choices=options,default='pending')

    def __str__(self):
        return self.user.username


class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='review')
    scrap=models.ForeignKey(Scrap,on_delete=models.CASCADE,related_name='scrap_review')
    comment=models.CharField(max_length=200)
    rating=models.CharField(max_length=100)

    def __str__(self):
        return self.comment
    

class Wishlist(models.Model):
    scrap=models.ForeignKey(Scrap,on_delete=models.CASCADE,related_name='scraps')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_wishlist')
    wishlists=models.ManyToManyField("self",related_name="cart_item",symmetrical=False,null=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.scrap