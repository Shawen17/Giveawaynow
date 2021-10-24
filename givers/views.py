from os import times
from typing import NewType
from django.forms import utils
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,GiveForm,ContactUsForm,Profileform,VendorForm
from .models import Profile,Give,ContactUs,Vendor
from django.http import HttpResponseRedirect,HttpResponse
import random
from django.contrib import messages
import os
from Giveaway.settings import STATIC_ROOT
from django.db.models import Sum
from time import sleep
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
import requests 
from .decorators import check_recaptcha


UserModel = get_user_model()



def home(request):
    return render(request,'givers/home.html')

def about(request):
    return render(request,'givers/about.html')

def signupuser(request):
    
    if request.method == 'POST':
        form = SignupForm()
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username Already Taken')
                return redirect('signupuser')
                
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email Already Exist')
                return redirect('signupuser')
                
            else:
                form = SignupForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    user.refresh_from_db()
                    user.profile.firstname=form.cleaned_data.get('firstname')
                    user.profile.lastname=form.cleaned_data.get('lastname')
                    user.profile.email=form.cleaned_data.get('email')
                    user.profile.phone_number=  form.cleaned_data.get('phone_number')
                    if not len(str(user.profile.phone_number)) == 10:
                        messages.error(request,'invalid phone number')
                        return redirect('signupuser')
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Activate your account.'
                    plaintext = template.loader.get_template('password/acc_activate_email.txt')
                    htmltemp = template.loader.get_template('password/acc_activate_email.html')
                    c = { 
					"email":user.profile.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Giveawaynow',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    text_content = plaintext.render(c)
                    html_content = htmltemp.render(c)
                    try:
                        msg = EmailMultiAlternatives(subject, text_content, 'Giveaway <admin@example.com>', [user.profile.email], headers = {'Reply-To': 'admin@example.com'})
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.info(request, "A verification mail has been sent to your email, kindly complete registration from there. ")
                    return redirect ("home")
                    '''username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password1')
                    user= authenticate(username=username,password=password)
                    login(request,user)
                    return redirect('account_update')'''
                else:
                    form = SignupForm()
                    messages.error(request,'form is invalid')
                    return redirect('signupuser')
                    
        else:
            messages.error(request,'Password does not match')
            return redirect('signupuser')
            
    else:
        form = SignupForm()
        return render(request, 'givers/signupuser.html',{'form':form})


def contact(request):
    
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Thanks, we will treat as urgent')
            return redirect('contact')
    else:
        form=ContactUsForm()
        return render(request,'givers/contact.html',{'form':form})


@login_required(login_url='/login/')
def user_account(request):
    user = request.user
    give=Give.objects.filter(gift_recipient=request.user.username,gift_status='redeemed')
    if len(give)==0:
        amount=''
    else:
        amt=[]
        for i in give:
            if i.gift.payment_status == False:
                if i.gift.amount is not None:
                    amt.append(i.gift.amount)
        if sum(amt)==0:
            amount=''
        else:
            amount=sum(amt,2000)
            
    all_gift = Give.objects.filter(user=user).count
    picks= Give.objects.filter(gift_recipient=user,date_requested__isnull=False)
    pick_count= Give.objects.filter(gift_recipient=user,date_requested__isnull=False).count
    gifts = Give.objects.filter(user=user, date_requested__isnull = True)
    mis_count = Give.objects.filter(user=user, date_requested__isnull = True).count
    return render(request,'givers/user_account.html',{'gifts':gifts,'user':user,'mis_count':mis_count,'picks':picks,'pick_count':pick_count,'all_gift':all_gift,'form':VendorForm(),'amount':amount})

@login_required(login_url='/login/')
def logoutuser(request):
    logout(request)
    return redirect('home')



'''def loginuser(request):
    if request.method == 'GET':
        return render(request, 'givers/loginuser.html', {'form':AuthenticationForm()})
    else:
        user= authenticate(request, username=request.POST['username'],password=request.POST['password']) 
        if user is None:
             return render(request, 'givers/loginuser.html', {'form':AuthenticationForm(),'error':'Username or Password incorrect'})
        else:
            login(request,user)
            if request.session.get('first_login'):
                return redirect('account_update')
            return redirect('user_account')'''


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'givers/loginuser.html', {'form':AuthenticationForm(),'recaptcha_site_key':settings.GOOGLE_RECAPTCHA_SITE_KEY})
    else:
        user= authenticate(request, username=request.POST['username'],password=request.POST['password']) 
        if user is None:
            messages.error(request,'Username or Password Incorrect')
            return redirect('loginuser')
            
        else:
            
            recaptcha_response = request.POST.get('g-recaptcha-response')
            print(recaptcha_response)
            data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response,
			}
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            print(result)
            if result['success']:
                login(request,user)
                if request.session.get('first_login'):
                    return redirect('account_update')
                return redirect('user_account')
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('loginuser')


@login_required(login_url='/login/')
def creategift(request):
    if request.method == 'GET':
        return render(request, 'givers/creategiving.html', {'form':GiveForm()})
    else:
        form = GiveForm(request.POST,request.FILES)
        if form.is_valid():
            new_gift = form.save(commit = False)
            new_gift.user = request.user
            new_gift.save()
            new_gift.gift.name = form.cleaned_data.get('name')
            new_gift.gift.category = form.cleaned_data.get('category')
            new_gift.gift.image = form.cleaned_data.get('image')
            new_gift.gift.giver_number = form.cleaned_data.get('giver_number')
            new_gift.gift.address = form.cleaned_data.get('address')
            if not len(str(new_gift.gift.giver_number)) == 10:
                        messages.error(request,'invalid phone number')
                        return redirect('creategift')
            new_gift.save()
            return redirect('giveaway')
        else:
            return render(request,'givers/creategiving.html',{'form':form,'error':'something went wrong'})

@login_required(login_url='/login/')
def giveaway(request):
    
    user=request.user
    gift1= Give.objects.filter(date_requested__isnull=True)
    query = request.GET.get('q')
    gifts= Give.objects.filter(Q(date_requested__isnull = True)&Q(state=user.profile.state)).order_by('-date_posted')
    if query:
        gifts = Give.objects.filter(Q(date_requested__isnull = True)&Q(state=user.profile.state)&Q(category__icontains=query)).order_by('-date_posted')
    
    p=Paginator(gifts,24)
    page_number=request.GET.get('page')
    try:
        page_obj=p.get_page(page_number)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)
    return render(request,'givers/giftpage.html',{'page_obj':page_obj,'user':user,'gift1':gift1})


@login_required(login_url='/login/')
def viewgift(request,gift_id):
    view = get_object_or_404(Give,pk = gift_id,user=request.user)
    if request.method == 'GET':
        form = GiveForm(instance=view)
        return render (request, 'givers/viewgift.html',{'view':view,'form':form})
    else:
        form = GiveForm(request.POST,instance=view)
        form.save()
        return redirect('user_account')

@login_required(login_url='/login/')
def edit_profile(request):
    user=request.user
    prof = get_object_or_404(Profile,user=request.user)
    if request.method == 'GET':
        profile_form= Profileform(instance=prof)
        return render (request, 'givers/account_update.html',{'user':user, 'profile_form':profile_form})
    else:
        profile_form = Profileform(request.POST,request.FILES,instance=prof)
        if  profile_form.is_valid():
            custom_form=profile_form.save(commit=False)
            custom_form.user=request.user
            custom_form.save()
            return redirect('user_account')
        else:
            return render(request,'givers/account_update.html',{'profile_form':profile_form,'error':'info not valid'})

@login_required(login_url='/login/')
def deletegift(request,gift_id):
    view = get_object_or_404(Give,user=request.user,pk=gift_id)
    if request.method == 'POST':
        view.delete()
        return redirect('user_account')


@login_required(login_url='/login/')
def pickgift(request,gift_id):
    user=request.user
    pick= get_object_or_404(Give,pk=gift_id)
    if request.method=='POST':
        pick.date_requested=timezone.now()
        pick.gift_recipient=str(user)
        pick.gift_status='requested'
        pick.save()
    return redirect('user_account')

@login_required(login_url='/login/')
def returnpicked(request,gift_id):
    view = get_object_or_404(Give,pk = gift_id)
    if request.method== 'POST':
        view.date_requested=None
        view.gift_recipient=''
        view.gift_status='unpicked'
        view.save(update_fields=['date_requested','gift_recipient','gift_status'])
        return redirect('user_account')

@login_required(login_url='/login/')
def viewpicked(request,gift_id):
    pick = get_object_or_404(Give,pk = gift_id)
    picked= get_object_or_404(Give,pk=gift_id)
    if request.method == 'GET':
        form = GiveForm(instance=pick)
        return render (request, 'givers/viewpicked.html',{'pick':pick,'form':form,'picked':picked})
    else:
        form = GiveForm(request.POST,instance=pick)
        form.save()
        return redirect('user_account')


@login_required(login_url='/login/')
def redeempicked(request,gift_id):
    
    user=request.user
    picked= get_object_or_404(Give,pk=gift_id)
    if request.method=='POST':
        characters=list('0123456789')
        characters.extend('abcdefghijklmnopqrstuvwxyz')
        characters.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        ticket=''
        for x in range(6):
            ticket +=random.choice(characters)
        form=VendorForm(request.POST,request.FILES,instance=picked)
        if form.is_valid:
            new_redeem=form.save()
            new_redeem.gift.ticket=ticket
            new_redeem.gift.request_date=timezone.now()
            new_redeem.gift.receiver_number=form.cleaned_data.get('receiver_number')
            new_redeem.gift.state=form.cleaned_data.get('state')
            new_redeem.gift.delivery_address=form.cleaned_data.get('delivery_address')
            new_redeem.save()
        elif 'return' in request.POST:
            picked.date_requested=None
            picked.gift_recipient=''
            picked.gift_status='unpicked'
            picked.save()
        elif 'mark' in request.POST:
            return redirect ('home')
    elif request.method=='GET':
        return render(request,'givers/text.html',{'form':VendorForm(instance=picked),'picked':picked})
    return redirect('user_account')
            
        
@login_required(login_url='/login/')       
def cancelpicked(request):
    gift_list = request.POST.getlist('chk[]')
    user=request.user
    if request.method=='POST':
        gifts =[int(x) for x in gift_list]
        instances = Give.objects.filter(id__in = gifts)
        data = {
                'date_requested':None,
                'gift_recipient': '',
                'gift_status':'unpicked'}
            
        if 'redeem' in request.POST:
            #using session to store checkbox variables
            request.session['gift_id'] = gifts
            '''file_path = os.path.join(STATIC_ROOT,f'givers\\{user}.txt')
            with open(file_path,'w') as f:
                f.writelines('%s\n' % i for i in gifts)'''
            return render(request,'givers/text.html',{'form':VendorForm()})
        elif 'return' in request.POST:
            for gift in instances:
                gift.date_requested= data['date_requested']
                gift.gift_recipient= data['gift_recipient']
                gift.gift_status=data['gift_status']
                gift.gift.ticket=''
                gift.gift.amount=None
                gift.gift.receiver_number=None
                gift.gift.delivery_address=None
                gift.gift.giver_contacted=False
                gift.gift.receiver_contacted=False
                gift.save()
        elif 'received' in request.POST:
            for gift in instances:
                if gift.gift.payment_status == True:
                    gift.gift.delivered= True
                    gift.save()
                else:
                    msg=f"you haven't paid for {gift.name} yet"
                    messages.error(request,msg)
                    return redirect('user_account')
    return redirect('user_account')


@login_required(login_url='/login/')
def redeem(request):
    shape=request.session.get('gift_id')
    user=request.user
    '''file_path = os.path.join(STATIC_ROOT,f'givers\\{user}.txt')
    shape=[]
    with open(file_path,'r') as f:
        for line in f:
            shape.append(int(line.strip('\n')))'''

    if request.method=='POST':
        characters=list('0123456789')
        characters.extend('abcdefghijklmnopqrstuvwxyz')
        characters.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        ticket=''
        for x in range(6):
            ticket +=random.choice(characters)
        give=Give.objects.get(id=shape[0])
        give.gift_status='redeemed'
        give.save()
        form=VendorForm(request.POST,request.FILES,instance=give)
        
        if form.is_valid:
            new_redeem=form.save()
            new_redeem.gift.ticket=ticket
            new_redeem.gift.request_date=timezone.now()
            new_redeem.gift.receiver_number=form.cleaned_data.get('receiver_number')
            new_redeem.gift.state=form.cleaned_data.get('state')
            new_redeem.gift.delivery_address=form.cleaned_data.get('delivery_address')
            new_redeem.save()
            if len(shape)>1:
                for id in shape[1:]:
                    give=Give.objects.get(id=id)
                    give.gift_status='redeemed'
                    give.save()
                    vend = Vendor.objects.get(give=give)
                    vend.ticket=ticket
                    vend.request_date=timezone.now()
                    vend.receiver_number=form.cleaned_data.get('receiver_number')
                    vend.state=form.cleaned_data.get('state')
                    vend.delivery_address=form.cleaned_data.get('delivery_address')
                    vend.save(update_fields=['ticket','request_date','receiver_number','delivery_address'])
                    
            else:
                new_redeem.gift.ticket=ticket
                new_redeem.gift.request_date=timezone.now()
                new_redeem.gift.receiver_number=form.cleaned_data.get('receiver_number')
                new_redeem.gift.state=form.cleaned_data.get('state')
                new_redeem.gift.delivery_address=form.cleaned_data.get('delivery_address')
                new_redeem.save()
    del request.session['gift_id']
    #os.remove(file_path)
    return redirect('user_account')


def my_mail(request):  
        subject = "Greetings from Programink"  
        msg     = "Learn Django at Programink.com"  
        to      = "shawen022@yahoo.com"  
        res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
        if(res == 1):  
            msg = "Mail Sent Successfully."  
        else:  
            msg = "Mail Sending Failed."  
        return HttpResponse(msg)  



'''def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Giveaway',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("password_reset")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request,"password/password_reset.html",{"password_reset_form":password_reset_form})'''

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data)|Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					plaintext = template.loader.get_template('password/password_reset_email.txt')
					htmltemp = template.loader.get_template('password/password_reset_email.html')
					c = { 
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Giveaway',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					text_content = plaintext.render(c)
					html_content = htmltemp.render(c)
					try:
						msg = EmailMultiAlternatives(subject, text_content, 'Giveaway <admin@example.com>', [user.email], headers = {'Reply-To': 'admin@example.com'})
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.info(request, "Password reset instructions have been sent to the email address entered.")
					return redirect ("home")
                
               
	password_reset_form = PasswordResetForm()
	return render(request,"password/password_reset.html",{"password_reset_form":password_reset_form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('loginuser')
    else:
        return HttpResponse('Activation link is invalid!')