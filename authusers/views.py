from interviewsquestions.settings import MEDIA_ROOT
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import TempUser,UserProfile,SocialUser
from random import randint
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout as _logout
from content.models import Category, Tag
import json
from interviewsquestions.utilities.authDecoratros import forActiveUser
import requests
from google.auth import jwt
def genRandomStr():
    str=''
    for i in range(0,99):
        str+=chr(randint(65,90))
    return str



def index(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active:
        if request.user.profile.tags.count()>0:
            return redirect(reverse('content:index'))
        else:
            return redirect(reverse('authusers:select-tags'))
    else:
        return redirect(reverse('authusers:login-page'))


def registerPage(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active:
        return redirect(reverse('authusers:auth-index'))
    if request.user.is_authenticated and not request.user.is_anonymous and not request.user.is_active:
        return redirect(reverse('authusers:email-sent'))

    if request.method== 'POST':
        fullName=request.POST['fullName'] if 'fullName' in request.POST else None
        userName=request.POST['userName'] if 'userName' in request.POST else None
        email=request.POST['email'] if 'email' in request.POST else None
        password=request.POST['password'] if 'password' in request.POST else None
        confirmPassword=request.POST['confirmPassword'] if 'confirmPassword' in request.POST else None
        emailTaken=User.objects.filter(email=email).exists()
        if fullName and userName and email and password and confirmPassword and password==confirmPassword and 'website' in request.POST and not emailTaken:
            website=request.POST['website']
            try:
                user=User.objects.create_user(userName,email,password,first_name=fullName,is_active=False)
                login(request,user)
                code=genRandomStr()
                TempUser.objects.create(user=user,code=code,website=website)
                msg= f"your confirm link: {request.build_absolute_uri(reverse('authusers:confirm-user',kwargs={'code':code}))}"
                send_mail("intervies questions",msg ,'interviewsquestions@gmail.com',[email])
                return redirect(reverse('authusers:email-sent') )
            except IntegrityError:
                messages.error(request,'User name is alredy exists',extra_tags='user-name')
          
        elif not fullName:
            messages.error(request,'Full name is requrid',extra_tags='full-name')
        elif not userName:
            messages.error(request,'User name is requrid',extra_tags='user-name')
        elif not email:
            messages.error(request,'Email is requrid',extra_tags='email')
        elif emailTaken:
            messages.error(request,'Email is taken',extra_tags='email')
        elif not password:
            messages.error(request,'Password is requrid',extra_tags='password')
        elif not confirmPassword:
            messages.error(request,'Confirm Password is requrid',extra_tags='conf-pass')
        elif not password== confirmPassword:
            messages.error(request,'Password does not match',extra_tags='conf-pass')
    return render(request,'auth/register.html')
def emailSent(request):
    
    if request.user.is_authenticated and not request.user.is_anonymous:
        if not request.user.is_active:
            contxt={
                'email':request.user.email
            }
            return render(request,'auth/emailSent.html',contxt)
    return redirect(reverse('authusers:auth-index'))
def confirmUser(request,code):
    try:
        tmpUser=TempUser.objects.get(code=code)
        user=tmpUser.user
        user.is_active=True
        user.save()
        profile=UserProfile()
        profile.user=user
        profile.website=tmpUser.website
        profile.save()
        tmpUser.delete()
    
        return redirect(reverse('authusers:auth-index'))
    except TempUser.DoesNotExist:
        return HttpResponse('invaid code')
def loginPage(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active:
        return redirect(reverse('authusers:auth-index'))
    elif request.user.is_authenticated and not request.user.is_anonymous and not request.user.is_active:
        return redirect(reverse('authusers:email-sent'))
    

    if request.method == 'POST':
        if 'email' in request.POST and 'password' in request.POST:
            user=authenticate(request,email=request.POST['email'],password=request.POST['password'])
       
            if user:
                if not user.is_active:
                    return redirect(reverse('authusers:email-sent'))
                if not user.profile.isBaned():
                    login(request,user)
                    if not 'remember' in request.POST:
                        request.session.set_expiry(0)
                    return redirect(reverse('authusers:auth-index'))
                else:
                    messages.error(request,'user baned')
            else:
                messages.error(request,"email or passowrd in not valid")
    return render(request,'auth/login.html')
def logout(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        _logout(request)
    return redirect(reverse('authusers:login-page'))
def selectTags(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active:
        if request.user.profile.tags.count()>0:
            return redirect(reverse('authusers:auth-index'))

        if request.method=='POST':
            if 'tags' in request.POST and 'category-id' in request.POST:
                userTags=json.loads(request.POST['tags'])
                if userTags:
                    try:
                        category=Category.objects.get(pk=int(request.POST['category-id']))
                        userProfile=request.user.profile
                        userProfile.category=category
                        for tagId in userTags:
                            userProfile.tags.add(Tag.objects.get(pk=int(tagId)))
                        return redirect(reverse('authusers:auth-index'))
                    except(Tag.DoesNotExist,Category.DoesNotExist,ValueError):
                        pass
                else:
                    messages.error(request,'you have to add 1 tag or more')
        tags=Tag.objects.all()
        categories=Category.objects.filter(parent=None)
        contxt={
            'tags':tags,
            'categories':categories
        }
        return render(request,'auth/selectTags.html',contxt)
    elif request.user.is_authenticated and not request.user.is_anonymous and not request.user.is_active:
        return redirect(reverse('authusers:email-sent'))
    else:
        return redirect(reverse('authusers:login-page'))
def chnageEmail(request):
    if request.user.is_authenticated and not request.user.is_anonymous and not request.user.is_active:
        if request.method=='POST':
            if 'email' in request.POST:
                if request.POST['email']:
                    if not User.objects.filter(email=request.POST['email']).exists() or request.user.email==request.POST['email']:
                        request.user.email=request.POST['email']
                        request.user.save()
                        
                        code=request.user.tmp.code
                        msg= f"your confirm link: {request.build_absolute_uri(reverse('authusers:confirm-user',kwargs={'code':code}))}"
                        send_mail("intervies questions",msg ,'interviewsquestions@gmail.com',[request.POST['email']])

                        return redirect(reverse('authusers:email-sent'))
                    else:
                        messages.error(request,'email is taken')
                else:
                    messages.error(request,'Email ir requrid')
        return render(request,'auth/changeEmail.html')
    else:
        return redirect(reverse('authusers:auth-index'))


def addSocialUser(request,registerPage,imageUrl):
    fullName=request.POST['fullName'] if 'fullName' in request.POST else None
    userName=request.POST['userName'] if 'userName' in request.POST else None
    email=request.POST['email'] if 'email' in request.POST else None
    password=request.POST['password'] if 'password' in request.POST else None
    confirmPassword=request.POST['confirmPassword'] if 'confirmPassword' in request.POST else None
    emailTaken= User.objects.filter(email=email).exists()
    if fullName and userName and email and password and confirmPassword and password==confirmPassword and 'website' in request.POST and not emailTaken:
        website=request.POST['website']
        try:
            user=User.objects.create_user(userName,email,password,first_name=fullName,is_active=True)
            profile=UserProfile()
            profile.user=user
            profile.website=website
            profile.socialID= request.POST["user-id"]
            imgResponse=requests.get(imageUrl)
            with open(str(MEDIA_ROOT.joinpath('profile'))+f'/{userName}.jpg','wb') as imgF:
                for chunk in imgResponse.iter_content(chunk_size=1024):
                    if chunk:
                        imgF.write(chunk)

            profile.image.name=str(MEDIA_ROOT.joinpath('profile'))+f'/{userName}.jpg'
            profile.save()
            if not profile.isBaned():

                login(request,user)
            else:
                messages.error(request,'user baned')
            return redirect(reverse('authusers:auth-index'))
        except IntegrityError:
            messages.error(request,'User name is alredy exists',extra_tags='user-name')

    elif not fullName:
        messages.error(request,'Full name is requrid',extra_tags='full-name')
    elif not userName:
        messages.error(request,'User name is requrid',extra_tags='user-name')
    elif not email:
        messages.error(request,'Email is requrid',extra_tags='email')
    elif emailTaken:
        messages.error(request,'Email is taken',extra_tags='email')
    elif not password:
        messages.error(request,'Password is requrid',extra_tags='password')
    elif not confirmPassword:
        messages.error(request,'Confirm Password is requrid',extra_tags='conf-pass')
    elif not password== confirmPassword:
        messages.error(request,'Password does not match',extra_tags='conf-pass')
    return registerPage


def addFacebookUser(request):
    if request.method=='POST':
        return addSocialUser(request,redirect(reverse('authusers:facebok-login'))
        ,f'https://graph.facebook.com/{request.POST["user-id"]}/picture?width=150&height=150')
    else:
        return redirect(reverse('authusers:auth-index'))

def facebookLogin(request):
    if not request.user.is_authenticated:
        if 'user-id' in request.POST and 'token' in request.POST:
            token=request.POST["token"]
            userID=request.POST["user-id"]
            try:
                profile=UserProfile.objects.get(socialID=userID)
                if not profile.isBaned():
                    login(request,profile.user)
                else:
                    messages.error(request,'user baned')
                return redirect(reverse('authusers:auth-index'))
                
            except UserProfile.DoesNotExist:
                respone=requests.get(f'https://graph.facebook.com/{userID}',
                params={
                    'access_token':token,
                    'fields':'id,name,email,picture'
                    })
                data=respone.json()
                try:
                    scocialUser=SocialUser.objects.create(fullName=data['name'],email=data['email'], image=f'https://graph.facebook.com/{userID}/picture?width=150&height=150',socialID=userID,provider='fa')            

                except IntegrityError:
                    pass
                context={
                    'fullName':data['name'],
                    'email':data['email'],
                    'image':f'https://graph.facebook.com/{userID}/picture?width=150&height=150',
                    'userID':userID,
                    'submitUrl':reverse('authusers:social-register'),
                    'provider':'fa'
                }
                return render(request,'auth/socialRegister.html',context)

          
    return redirect(reverse('authusers:auth-index'))




def googelLogin(request):
    if not request.user.is_authenticated:
        if 'jwt' in request.POST:
            data=jwt.decode(request.POST['jwt'],verify=False)
            userID=data['sub']
            try:
                profile=UserProfile.objects.get(socialID=userID)
                if not profile.isBaned():
                    login(request,profile.user)
                else:
                    messages.error(request,'user baned')
                return redirect(reverse('authusers:auth-index'))
                
            except UserProfile.DoesNotExist:
                try:
                    socialUser=SocialUser.objects.create(fullName=data['name'],email=data['email'],image=data['picture'],socialID=data['sub'],provider='go')
                except IntegrityError:
                    pass


                
                
            context={
                'fullName':data['name'],
                'email':data['email'],
                'image':data['picture'],
                'userID':userID,
                'submitUrl':reverse('authusers:social-register'),
                'provider':'go'
            }
            return render(request,'auth/socialRegister.html',context)

    return redirect(reverse('authusers:auth-index'))


def githubLogin(request):
    if not request.user.is_authenticated:
        if 'code' in request.GET:
            code=request.GET['code']
            response=requests.post('https://github.com/login/oauth/access_token',data={
                'client_id':'325f252be688f7172df1',
                'client_secret':'9645d48a16f0966a30dc8831447c8fc7cbe56625',
                'code':code
            },headers={'Accept':'application/json'})
            try:
                token=response.json()['access_token']
                request.session['git-token']=token 
            except KeyError:
                token=request.session['git-token']
            responseData=requests.post('https://api.github.com/user',headers={'Authorization': f'token {token}'})
            data=responseData.json()
            username=data['login']
            userID=data['id']
            name=data['name'] if not data['name']=='null' else None
            imageUrl=data['avatar_url']
            responseEmail=requests.get('https://api.github.com/user/emails',headers={'Authorization': f'token {token}'})
            email=responseEmail.json()[0]['email']

        try:
            profile=UserProfile.objects.get(socialID=userID)
            if not profile.isBaned():

                login(request,profile.user)
            else:
                messages.error(request,'user baned')
            return redirect(reverse('authusers:auth-index'))
            
        except UserProfile.DoesNotExist:
            try:
                socialUser=SocialUser.objects.create(fullName=name,email=email,image=imageUrl,socialID=userID,provider='gi')
            except IntegrityError:
                pass
            context={
                'fullName':name,
                'email':email,
                'image':imageUrl,
                'userID':userID,
                'submitUrl':reverse('authusers:social-register'),
                'provider':'gi'
            }
            return render(request,'auth/socialRegister.html',context)

        
    return redirect(reverse('authusers:auth-index'))


def regisetSocialUser(request):
    if not request.user.is_authenticated:

        if 'provider' in request.POST and 'user-id' in request.POST:
            socialUser=SocialUser.objects.get(socialID=request.POST['user-id'],provider=request.POST['provider'])
    
            fullName= socialUser.fullName if socialUser.fullName else request.POST['fullName'] if 'fullName' in request.POST else None
            userName=request.POST['userName'] if 'userName' in request.POST else None
            email= socialUser.email
            password=request.POST['password'] if 'password' in request.POST else None
            confirmPassword=request.POST['confirmPassword'] if 'confirmPassword' in request.POST else None
            emailTaken= User.objects.filter(email=email).exists()
            if fullName and userName and email and password and confirmPassword and password==confirmPassword and 'website' in request.POST and not emailTaken:
                website=request.POST['website']
                try:
                    user=User.objects.create_user(userName,email,password,first_name=fullName,is_active=True)
                    profile=UserProfile()
                    profile.user=user
                    profile.website=website
                    profile.socialID= request.POST["user-id"]
                    imgResponse=requests.get(socialUser.image)
                    with open(str(MEDIA_ROOT.joinpath('profile'))+f'/{userName}.jpg','wb') as imgF:
                        for chunk in imgResponse.iter_content(chunk_size=1024):
                            if chunk:
                                imgF.write(chunk)

                    profile.image.name=f'profile/{userName}.jpg'
                    profile.save()
                    socialUser.delete()
                    if not profile.isBaned():

                        login(request,user)
                    else:
                        messages.error(request,'user baned')
                    return redirect(reverse('authusers:auth-index'))
                    
                except IntegrityError:
                    messages.error(request,'User name is alredy exists',extra_tags='user-name')

            elif not fullName:
                messages.error(request,'Full name is requrid',extra_tags='full-name')
            elif not userName:
                messages.error(request,'User name is requrid',extra_tags='user-name')
            elif not email:
                messages.error(request,'Email is requrid',extra_tags='email')
            elif emailTaken:
                messages.error(request,'Email is taken',extra_tags='email')
            elif not password:
                messages.error(request,'Password is requrid',extra_tags='password')
            elif not confirmPassword:
                messages.error(request,'Confirm Password is requrid',extra_tags='conf-pass')
            elif not password== confirmPassword:
                messages.error(request,'Password does not match',extra_tags='conf-pass')

            context={
                'fullName':socialUser.fullName,
                'email':socialUser.email,
                'image':socialUser.image,
                'userID':socialUser.socialID,
                'submitUrl':reverse('authusers:social-register'),
                'provider':socialUser.provider
            }
            return render(request,'auth/socialRegister.html',context)

 
    return redirect(reverse('authusers:auth-index'))



def checkAuthentication(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active:
        return HttpResponse('1')
    else:
        return HttpResponse('0')