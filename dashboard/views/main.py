from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout as  logoutAuth
from django.urls import reverse
from django.utils.translation import gettext

def index(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        return render(request,'utilities/dashboard/_base.html')
    else:
        return redirect(reverse('dashboard:login'))
def loginPage(request):

    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        return redirect(reverse('dashboard:index'))
    else:
        if request.method=='POST':
            if 'email' in request.POST and 'password' in request.POST:
                user=authenticate(request,email=request.POST['email'],password=request.POST['password'])
                if user and user.is_superuser:
                    if not 'rememberme' in request.POST:
                        request.session.set_expiry(0)
                    login(request,user)
                    return redirect(reverse('dashboard:index'))

                elif not user:
                    messages.error(request,gettext('invalid email or password'))
                elif not user.is_superuser:
                    messages.error(request,gettext('This page for only admin '))
            elif not 'email' in request.POST:
                messages.error(request,gettext('Email is requreid'))
            elif not 'password' in request.POST:
                messages.error(request,gettext('Password is requreid'))
        return render(request,'dashboard/login.html')

def logout(request):
    if request.user.is_authenticated:
        logoutAuth(request)
    return redirect("/dashboard/login") # TODO redirect to site 


