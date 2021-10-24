from django.contrib import admin
from .models import Profile,Give,GiveImage,ContactUs,Received,Vendor,Transaction
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User



@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display=('order_id','made_by','made_on','amount','checksum')
    ordering =('-made_on',)
    search_fields =('order_id',)

@admin.register(Received)
class ReceivedAdmin(ModelAdmin):
    list_display =('gift_requested','date_requested','date_received')
    ordering = ('-date_requested','-date_received')
    search_fields = ('gift_requested',)

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display =('ticket','email','subject','body','date')
    ordering =('-date','subject',)
    search_fields = ('email','ticket')

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display=('firstname','lastname','email','state','phone_number','sex','profile_pic','bio','date_joined')
    search_fields=('state','date_joined')
    ordering = ('-date_joined',)

class ProfileInline(admin.StackedInline):
    model=Profile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'profile'



class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    

class GiveImageInline(admin.StackedInline):
    model=GiveImage
    fk_name= 'give'
    can_delete= False
    verbose_name_plural = 'giveimage'

class VendorInline(admin.StackedInline):
    model= Vendor
    fk_name= 'give'
    can_delete = False
    verbose_name_plural= 'gift'

@admin.register(Give)
class GiveAdmin(ModelAdmin):
    inlines=(GiveImageInline,VendorInline)
    list_display= ('name','category','gift_recipient','state','address','description','image','quantity','giver_number','date_posted','date_requested','date_received','gift_status')
    search_fields=('category','date_requested','gift_status',)
    ordering=('-date_posted','category',)
    actions = ['mark_received','mark_unpicked']

    
    def mark_received(self,request,queryset):
        queryset.update(gift_status='received')

    def mark_unpicked(self,request,queryset):
        queryset.update(gift_status='unpicked')

    mark_unpicked.short_description='Mark as Unpicked'
    mark_received.short_description = 'Mark as Received'
  

@admin.register(GiveImage)
class GiveImageAdmin(ModelAdmin):
    pass


@admin.register(Vendor)
class VendorAdmin(ModelAdmin):
    list_display=('ticket','give','name','image','category','request_date','giver_number','address','giver_contacted','receiver_number','receiver_contacted','delivery_address','amount','payment_status','delivered')
    ordering=('-request_date','delivered')
    search_fields=('ticket',)
    actions=['mark_giver','mark_receiver','mark_payment','mark_delivered']

    def mark_giver(self,request,queryset):
        queryset.update(giver_contacted=True)

    def mark_receiver(self,request,queryset):
        queryset.update(receiver_contacted=True)

    def mark_payment(self,request,queryset):
        queryset.update(payment_status=True)

    def mark_delivered(self,request,queryset):
        queryset.update(delivered=True)

    mark_giver.short_description='Mark Giver as Contacted'
    mark_receiver.short_description = 'Mark Receiver as Contacted'
    mark_payment.short_description = 'Mark as Paid'
    mark_delivered.short_description = 'Mark as Delivered'




admin.site.unregister(User)
admin.site.register(User,UserAdmin)

