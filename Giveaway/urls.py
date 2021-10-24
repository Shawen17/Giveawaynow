"""Giveaway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include,register_converter
from  django.conf import settings
from django.conf.urls.static import static
from givers import views
from django.conf.urls import url
from django.views.static import serve
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('signup/',views.signupuser,name='signupuser'),
    path('login/',views.loginuser,name='loginuser'),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('account/',views.user_account, name= 'user_account'),
    path('add/',views.creategift,name='creategift'),
    path('giveaway/',views.giveaway, name='giveaway'),
    path('gifts/<int:gift_id>/view',views.viewgift, name='viewgift'),
    path('profile/edit', views.edit_profile, name='account_update'),
    path('gifts/<int:gift_id>/delete',views.deletegift, name='deletegift'),
    path('pick/<int:gift_id>/gift',views.pickgift, name='selectgift'),
    path('view/<int:gift_id>/picked',views.viewpicked, name='viewpicked'),
    path('return/<int:gift_id>/picked',views.returnpicked, name='returnpicked'),
    path('gift/<int:gift_id>/redeem',views.redeempicked, name='redeempicked'),
    path('gift/return',views.cancelpicked, name='cancelpicked'),
    path('gift/redeem',views.redeem,name='redeemgift'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('blog/',include('blog.urls'),name='blog'),
    path('social-oauth/',include('social_django.urls'),name='social'),
    path('mail/',views.my_mail,name='mail'),
    path('', include('givers.urls')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('accounts/', include('allauth.urls')),
]










urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
