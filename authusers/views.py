from PIL import Image
from interviewsquestions.settings import MEDIA_ROOT
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import AuthList, TempUser,UserProfile,SocialUser,TmpLink
from random import randint
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout as _logout
from content.models import Badge, Category, Tag
import json
from interviewsquestions.utilities.authDecoratros import forActiveUser
import requests
from google.auth import jwt
from django.utils.translation import get_language,gettext
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
                respone= redirect(reverse('authusers:email-sent') )
                code=genRandomStr()
                tmp=TempUser.objects.create(user=user,code=code,website=website)
                respone.set_cookie('tmp-id',user.id)
                msg= f"your confirm link: {request.build_absolute_uri(reverse('authusers:confirm-user',kwargs={'code':code}))}"
                send_mail("intervies questions",msg ,'interviewsquestions@gmail.com',[email])
                return respone
            except IntegrityError:
                messages.error(request,gettext('User name is alredy exists'),extra_tags='user-name')
          
        elif not fullName:
            messages.error(request,gettext('Full name is requrid'),extra_tags='full-name')
        elif not userName:
            messages.error(request,gettext('User name is requrid'),extra_tags='user-name')
        elif not email:
            messages.error(request,gettext('Email is requrid'),extra_tags='email')
        elif emailTaken:
            messages.error(request,gettext('Email is taken'),extra_tags='email')
        elif not password:
            messages.error(request,gettext('Password is requrid'),extra_tags='password')
        elif not confirmPassword:
            messages.error(request,gettext('Confirm Password is requrid'),extra_tags='conf-pass')
        elif not password== confirmPassword:
            messages.error(request,gettext('Password does not match'),extra_tags='conf-pass')
    contxt={
        'list':AuthList.objects.get(page='R',language=get_language()[:2])
    }
 
    return render(request,'auth/register.html',contxt)
def emailSent(request):
    
    if request.COOKIES.get('tmp-id',None):
        if not request.user.is_active:
            contxt={
                'email':User.objects.get(pk=request.COOKIES.get('tmp-id')).email
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
        login(request,user)
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
                    if user.is_active:

                        countLoginBadges(user)

                    if not 'remember' in request.POST:
                        request.session.set_expiry(0)
                    return redirect(reverse('authusers:auth-index'))
                else:
                    messages.error(request,gettext('user baned'))
            else:
                messages.error(request,gettext("email or passowrd in not valid"))
    contxt={
        'list':AuthList.objects.get(page='L',language=get_language()[:2])
    }
 
    return render(request,'auth/login.html',contxt)
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
                    messages.error(request,gettext('you have to add 1 tag or more'))
        language=get_language()[:2]
        tags=Tag.objects.filter(category__language=language)
        categories=Category.objects.filter(parent=None,language=language)
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
    if request.COOKIES.get('tmp-id',None):
        user=User.objects.get(pk=request.COOKIES.get('tmp-id',None))
        if  not user.is_active:
            if request.method=='POST':
                if 'email' in request.POST:
                    if request.POST['email']:
                        if not User.objects.filter(email=request.POST['email']).exists() or user.email==request.POST['email']:
                            user.email=request.POST['email']
                            user.save()
                            
                            code=user.tmp.code
                            msg= f"your confirm link: {request.build_absolute_uri(reverse('authusers:confirm-user',kwargs={'code':code}))}"
                            send_mail("intervies questions",msg ,'interviewsquestions@gmail.com',[request.POST['email']])

                            return redirect(reverse('authusers:email-sent'))
                        else:
                            messages.error(request,gettext('email is taken'))
                    else:
                        messages.error(request,gettext('Email is requrid'))
            return render(request,'auth/changeEmail.html')
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
                    countLoginBadges(profile.user)

                else:
                    messages.error(request,gettext('user baned'))
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
                    countLoginBadges(profile.user)

                else:
                    messages.error(request,gettext('user baned'))
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
                countLoginBadges(profile.user)

            else:
                messages.error(request,gettext('user baned'))
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
                    profile.provider=request.POST['provider']
                    imgResponse=requests.get(socialUser.image)
                    with open(str(MEDIA_ROOT.joinpath('profile'))+f'/{userName}.jpg','wb') as imgF:
                        for chunk in imgResponse.iter_content(chunk_size=1024):
                            if chunk:
                                imgF.write(chunk)
                    profile.image.name=f'profile/{userName}.jpg'
                    resizedImag=Image.open(str(MEDIA_ROOT.joinpath('profile'))+f'/{userName}.jpg')
                    resizedImag=resizedImag.resize((35,35))
                    resizedImag.save(str(MEDIA_ROOT.joinpath('profile'))+f'/sm-{userName}.jpg')
                    profile.save()
                    socialUser.delete()

                    login(request,user)


                    
                except IntegrityError:
                    messages.error(request,gettext('User name is alredy exists'),extra_tags='user-name')

            elif not fullName:
                messages.error(request,gettext('Full name is requrid'),extra_tags='full-name')
            elif not userName:
                messages.error(request,gettext('User name is requrid'),extra_tags='user-name')
            elif not email:
                messages.error(request,gettext('Email is requrid'),extra_tags='email')
            elif emailTaken:
                messages.error(request,gettext('Email is taken'),extra_tags='email')
            elif not password:
                messages.error(request,gettext('Password is requrid'),extra_tags='password')
            elif not confirmPassword:
                messages.error(request,gettext('Confirm Password is requrid'),extra_tags='conf-pass')
            elif not password== confirmPassword:
                messages.error(request,gettext('Password does not match'),extra_tags='conf-pass')
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



def countLoginBadges(user):
    user.profile.loginTimes+=1
    user.profile.save()

    badges=Badge.objects.filter(reason=Badge.reasons.LoginTimes)
    badges=badges.difference(user.profile.badges.all())
    for badge in badges:
        if user.profile.loginTimes>= badge.count:
            user.profile.badges.add(badge)



def resetPassword(request):
        
    if request.user.is_authenticated and not request.user.is_anonymous:
        return redirect(reverse('content:index'))
    if 'email' in request.POST and 'g-recaptcha-response' in request.POST:
        response=requests.post('https://www.google.com/recaptcha/api/siteverify',data={
                'secret':'6LeJxbwcAAAAADv0EJ_w2cibGxhFlX-aFvdyysWz',
                'response':request.POST['g-recaptcha-response']
            })
        if response.json()['success']:
            try:
                user =User.objects.get(email=request.POST['email'])
                link=TmpLink.objects.create(user=user,key=genRandomStr())
                send_mail('Reset Your Password',f'{request.build_absolute_uri("/set-password")}?key={link.key}',None,[user.email])
                return redirect(reverse('authusers:email-sent'))
            except User.DoesNotExist:
                messages.error(request,gettext('No account with this email'))
        else:
            messages.error(request,gettext('invalid captcha'))
    return render(request,'auth/resetPassword.html')

def setPassword(request):

    if request.method == 'POST':
        if 'key' in request.POST and 'password' in request.POST and 'conf-password' in request.POST:
            if request.POST['password'] and request.POST['conf-password'] and request.POST['password'] == request.POST['conf-password']:
                

                try:
                    link=TmpLink.objects.get(key=request.POST['key'])
                    user=link.user 
                    user.set_password(request.POST['password'])
                    user.save()
                    link.delete()
                    return redirect('authusers:login-page')
                except TmpLink.DoesNotExist:
                    pass   

            elif  not request.POST['password']:
                messages.error(request,gettext('Password is requrid'),extra_tags='password')

            elif not request.POST['conf-password']:
                messages.error(request,gettext('Confirm Password is requrid'),extra_tags='conf-pass')
            elif not request.request.POST['password'] == request.request.POST['conf-password']:
                messages.error(request,gettext('Password does not match'),extra_tags='conf-pass')
    if request.method == 'GET':    
        if 'key' in request.GET:
            try:
                link=TmpLink.objects.get(key=request.GET['key'])
                contxt={
                    'key':link.key
                }
                return render(request,'auth/changePassword.html',contxt)
            except TmpLink.DoesNotExist:
                pass
    return HttpResponse('invaild key')