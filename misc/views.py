from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse

from .models import InfoItem,Service,ContactMessage,AdvertisePage,AdvertistRequest
from django.contrib import messages
from django.utils.translation import get_language,gettext
def InfoPage(request):
    language=get_language()[:2].upper()
    items=InfoItem.objects.filter(language=language)
    contxt={
        'items':items
    }
    return render(request,'misc/info.html',contxt)


def servicesPage(request):
    language=get_language()[:2].upper()
    services=Service.objects.filter(language=language)
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
        page=AdvertisePage.objects.get(language=language)
    except AdvertisePage.DoesNotExist:
        return HttpResponse('this page not created yet')
    contxt={
        'page':page
    }

    return render(request,'misc/advertise.html',contxt)