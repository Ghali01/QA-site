from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse

from .models import InfoItem,Service,ContactMessage,AdvertisePage,AdvertistRequest, TermsPage
from django.contrib import messages
from django.utils.translation import get_language,gettext
from django.core.cache import cache
def InfoPage(request):
    language=get_language()[:2].upper()
    items=cache.get(f'info-{language}')
    if items==None:
        items=InfoItem.objects.filter(language=language)
        cache.set(f'info-{language}',items)
    contxt={
        'items':items
    }
    return render(request,'misc/info.html',contxt)


def servicesPage(request):
    language=get_language()[:2].upper()
    services=cache.get(f'services-{language}')
    if services==None:   
        services=Service.objects.filter(language=language)
        cache.set(f'services-{language}',services)
    contxt={
        'services':services
    }
    return render(request,'misc/services.html',contxt)

def contactUS(request):
    if request.method == 'POST':
        if 'fullName' in request.POST and 'email' in request.POST and 'subject' in request.POST and 'msg' in request.POST:
            fullName=request.POST['fullName']
            email=request.POST['email']
            subject=request.POST['subject']
            msgText=request.POST['msg']
            if fullName and email and subject and msgText:
                ContactMessage.objects.create(
                    userName=fullName,
                    email=email,
                    subject=subject,
                    text=msgText
                )
                messages.success(request,gettext('message sent'))
            else:
                messages.error(request,gettext("check empty fields"))

        else:
            messages.error(request,gettext("check empty fields"))
    return render(request,'misc/contactUs.html')


def advertiseWithUs(request):
    language=get_language()[:2].upper()
    if request.method=='POST':
        if 'companyName' in request.POST and 'email' in request.POST and 'subject' in request.POST and 'msg' in request.POST:
            companyName=request.POST['companyName']
            email=request.POST['email']
            subject=request.POST['subject']
            msgText=request.POST['msg']
            if companyName and email and subject and msgText:
                AdvertistRequest.objects.create(
                    company=companyName,
                    email=email,
                    subject=subject,
                    text=msgText,
                    language=language
                )
                messages.success(request,gettext('message sent'))
            else:
                messages.error(request,gettext("check empty fields"))
    try:

        page=cache.get(f'advertise-{language}')
        if page == None:
            page=AdvertisePage.objects.get(language=language)
            cache.set(f'advertise-{language}',page)
    except AdvertisePage.DoesNotExist:
        return HttpResponse('this page not created yet')
    contxt={
        'page':page
    }

    return render(request,'misc/advertise.html',contxt)


def terms(request):
    language=get_language()[:2]
    page=cache.get(f'terms-{language}')
    if page==None:
        page=TermsPage.objects.get(language=language)
        cache.set(f'terms-{language}',page)
    contxt={
        'terms':page.html
    }
    return render(request,'misc/terms.html',contxt)