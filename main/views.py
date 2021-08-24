
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import TempUser
from random import randint
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.urls import reverse
def genRandomStr():
    str=''
    for i in range(0,99):
        str+=chr(randint(65,90))
    return str
def registerPage(request):
    if request.method== 'POST':
        fullName=request.POST['fullName'] if 'fullName' in request.POST else None
        userName=request.POST['userName'] if 'userName' in request.POST else None
        email=request.POST['email'] if 'email' in request.POST else None
        password=request.POST['password'] if 'password' in request.POST else None
        confirmPassword=request.POST['confirmPassword'] if 'confirmPassword' in request.POST else None
        if fullName and userName and email and password and confirmPassword and password==confirmPassword and 'website' in request.POST:
            website=request.POST['website']
            try:
                user=User.objects.create_user(userName,email,password,first_name=fullName,is_active=False)
                code=genRandomStr()
                TempUser.objects.create(user=user,code=code,website=website)
                msg= f"your confirm link: {request.build_absolute_uri(reverse('confirm-user',kwargs={'code':code}))}"
                return HttpResponse(msg)
                # send_mail("intervies questions",msg ,'interviewsquestions@gmail.com',[email])
            except IntegrityError:
                messages.error(request,'User name is alredy exists',extra_tags='user-name')

        elif not fullName:
            messages.error(request,'Full name is requrid',extra_tags='full-name')
        elif not userName:
            messages.error(request,'User name is requrid',extra_tags='user-name')
        elif not email:
            messages.error(request,'Email is requrid',extra_tags='email')
        elif not password:
            messages.error(request,'Password is requrid',extra_tags='password')
        elif not confirmPassword:
            messages.error(request,'Confirm Password is requrid',extra_tags='conf-pass')
        elif not password== confirmPassword:
            messages.error(request,'Password does not match',extra_tags='conf-pass')
    return render(request,'auth/register.html')
def emailSent(request):
    return render(request,'auth/emailSent.html')
def confirmUser(request,code):
    try:
        tmpUser=TempUser.objects.get(code=code)
        user=tmpUser.user
        user.is_active=True
        user.save()
        tmpUser.delete()
        return redirect(reverse('login-page'))
    except TempUser.DoesNotExist:
        return HttpResponse('invaid code')
def loginPage(request):
    return render(request,'auth/login.html')