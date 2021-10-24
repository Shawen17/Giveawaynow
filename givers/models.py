from django.db import models
from django import dispatch
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import pandas as pd
from Giveaway.settings import STATIC_ROOT
from django.utils import timezone
from  django.core.exceptions import ValidationError
import gettext as _



def validate_num(value):
    value=str(value)
    if len(value) != 11 or value[0] != 0:
        value=int(value)
        raise ValidationError(
            _('%(value)s is not a valid number'),
            code='invalid number',
            params={'value':value},
        )





file_path = os.path.join(STATIC_ROOT,'givers\\state.xlsx')
df = pd.read_excel(file_path)
df1= zip(df.value,df.representation)
states=[]
for i,j in df1:
    states.append((i,j))

file_path = os.path.join(STATIC_ROOT,'givers\\vendor.xlsx')
df = pd.read_excel(file_path)
df1= zip(df.value,df.representation)
vendors=[]
for i,j in df1:
    vendors.append((i,j))



com_list=(
    ('enquiry','Enquiry'),
    ('complaint','Complaint'),
    ('report','Report'),
    ('others','Others')
)

gender =(
    ('male','Male'),
    ('female','Female')
)

categories =(
    ('furniture','Furniture'),
    ('clothe','Clothes'),
    ('shoe','Shoes'),
    ('toy','toys'),
    ('electronics','Electronics'),
    ('bags','Bags'),
    ('mobile','mobile-phones'),
    ('laptop','Laptops'),
    ('book','Books'),
    ('kitchen-utensils','Kitchen-utensils'),
    ('bicycle','Bicyle'),
    ('accessories','Accessories'),
    ('food-stuffs','Food-stuffs'),
    ('groceries','Groceries'),
    ('generator','Generator'),
    ('beauty-product','Beauty-product'),
)

status=(
    ('unpicked','unpicked'),
    ('requested','requested'),
    ('received','received'),
    ('redeemed','redeemed')

)

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    firstname = models.CharField(max_length=100,blank=True,default='')
    lastname = models.CharField(max_length=100,blank=True,default='')
    email =models.EmailField(max_length=150)
    state=models.CharField(max_length=50,choices=states,blank=True,default='')
    phone_number=models.BigIntegerField(default=int('08000000000'))
    sex=models.CharField(max_length=10,choices=gender,blank=True,default='')
    profile_pic = models.ImageField(upload_to='givers/images',default='default_pic.jpg')
    bio = models.TextField(blank=True,default='')
    date_joined=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    '''def clean(self):
        value=str(self.phone_number)
        if not len(value) == 10 :
            raise ValidationError({'phone_number':'invalid number'})

    def save(self,*args,**kwargs):
        self.full_clean()
        return super().save(*args,**kwargs)'''


@receiver(post_save,sender=User,dispatch_uid='user.created')   
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Give(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    state=models.CharField(max_length=40,choices=states)
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=50,blank=True,default='',choices=categories)
    description = models.TextField()
    image= models.ImageField(blank=True)
    quantity=models.IntegerField()
    giver_number=models.BigIntegerField(default='')
    address=models.TextField(default='')
    date_posted=models.DateTimeField(auto_now_add=True)
    date_requested = models.DateTimeField(null=True,blank=True)
    date_received = models.DateTimeField(null=True,blank=True)
    gift_recipient = models.CharField(max_length=100,default='',blank=True)
    gift_status = models.CharField(max_length=30,default='unpicked',blank=True,choices=status)

    def __str__(self):
        return self.name

class GiveImage(models.Model):
    give= models.ForeignKey(Give,default=None,on_delete=models.CASCADE,related_name='giveimage')
    images= models.ImageField(upload_to='givers/images/')

    def __str__(self):
        return self.giveimage.give


class ContactUs(models.Model):
    ticket=models.CharField(max_length=15,blank=True,default='')
    email= models.EmailField(max_length=150)
    subject= models.CharField(max_length=20,choices=com_list)
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Received(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='person')
    gift_requested = models.OneToOneField(Give,on_delete=models.CASCADE,related_name='commodity')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_received = models.DateTimeField(auto_now_add=True)


class Vendor(models.Model):
    give = models.OneToOneField(Give,on_delete=models.CASCADE,related_name='gift')
    #user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    #profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='profile')
    ticket = models.CharField(max_length=10)
    image=models.ImageField(upload_to='givers/images/')
    #vendor_name=models.CharField(max_length=100,choices=vendors,default='')
    state = models.CharField(max_length=50,choices=states,default='')
    name=models.CharField(max_length=100)
    request_date=models.DateTimeField(blank=True,null=True)
    category = models.CharField(max_length=100,choices=categories)
    giver_number=models.BigIntegerField(blank=True,null=True)
    address=models.TextField(default='')
    receiver_number=models.BigIntegerField(blank=True,null=True)
    giver_contacted=models.BooleanField(default=False)
    receiver_contacted=models.BooleanField(default=False)
    delivery_address =models.TextField(max_length=200,blank=True,null=True)
    amount = models.BigIntegerField(blank=True,null=True)
    payment_status = models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)

    def __str__(self):
        return self.give.name


@receiver(post_save,sender=Give,dispatch_uid='give.created')   
def create_vendor_profile(sender,instance,created,**kwargs):
    if created:
        Vendor.objects.create(give=instance)
    instance.gift.save()


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)




