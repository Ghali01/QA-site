from typing import Callable
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout as  logoutAuth
from django.urls import reverse
from django.utils.translation import gettext
from authusers.models import SocialProviders, UserProfile
from content.models import Category, Question, Tag
from dashboard.decorators import forSuperAdmin
from dashboard.models import BoolOption
from feedback.models import SuggestedCategory, SuggestedTag
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
    return redirect("/dashboard/login") 



@forSuperAdmin
def options(request):
    if request.method=='POST':
        BoolOption.setArabic('arabic-pub' in request.POST)
        return redirect(reverse('dashboard:restart-server'))
    return render(request,'dashboard/options.html',{'araOpt':BoolOption.arabicOn()})




from threading import Timer
import os
@forSuperAdmin
def restaratServer(request):

    Timer(5,lambda:os.system("systemctl restart  emperor.usgi.service")).start()
    return render(request,'dashboard/restartServer.html')

@forSuperAdmin
def statistics(request,language):
    contxt={
        'questions':Question.objects.filter(category__language=language).count(),
        'tags':Tag.objects.filter(category__language=language).count(),
        'categories':Category.objects.filter(language=language).count(),
        'questionsFE':Question.objects.filter(category__language=language,forExams=True).count(),
        'allUsers':UserProfile.objects.filter(language=language).count(),
        'EMUsers':UserProfile.objects.filter(language=language,provider=None).count(),
        'FAUsers':UserProfile.objects.filter(language=language,provider=SocialProviders.Facebook).count(),
        'GOUsers':UserProfile.objects.filter(language=language,provider=SocialProviders.Google).count(),
        'GIUsers':UserProfile.objects.filter(language=language,provider=SocialProviders.Github).count(),
        'suggestedCategories':SuggestedCategory.objects.filter(language=language).count(),
        'suggestedTags':SuggestedTag.objects.filter(category__language=language).count(),
 
    }
    return render(request,'dashboard/statistics.html',contxt)