from django.shortcuts import render,redirect
from django.urls.conf import path
from misc.models import ContactMessage,AdvertistRequest
from math import ceil
from django.http import HttpResponse

def contactMessage(request,language,page):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        messagesSet=ContactMessage.objects.filter(language=language)
        page=1 if page==0 else page
        count=messagesSet.count()+0
        toN=page*25
        fromN=toN-25
        messagesSet=list(messagesSet)[fromN:toN]
        indcStart=page-3 if page>=4 else 1
        pagesCuont=ceil(count/25)
        remPages=ceil((count-fromN)/25)
        if page>pagesCuont and remPages: return redirect(f'/dashboard/contact-messages/{language}/1')
        pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
       
        contxt={
            'lang':language,
            'msgs':messagesSet,
            'pages':pages if len(pages)>1 else [],
            'currentPage':page

        }
        return render(request,'dashboard/contactMessages.html',contxt)
    else:
        return redirect("/dashboard/login")

def deleteContactMessage(request,language,page):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'message-id' in request.POST:
            try:
                msg=ContactMessage.objects.get(pk=int(request.POST['message-id']))
                msg.delete()
                return redirect(f'/dashboard/contact-messages/{language}/{page}')
            except (ContactMessage.DoesNotExist,ValueError):
                return HttpResponse("ID is not valid1")
        else:
            return HttpResponse("ID is not valid2")

    else:
        return redirect("/dashboard/login")


def showContactMessage(request,messageID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        try:
            theMessage=ContactMessage.objects.get(pk=messageID)
            contxt={
                'theMessage':theMessage
            }
            return render(request,'dashboard/contactMessage.html',contxt)
        except (ContactMessage.DoesNotExist,ValueError):
            return HttpResponse("ID is not valid")
    else:
        return redirect("/dashboard/login")


def advertiseMessage(request,language,page):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        requests=AdvertistRequest.objects.filter(language=language)
        page=1 if page==0 else page
        count=requests.count()+0
        toN=page*25
        fromN=toN-25
        requests=list(requests)[fromN:toN]
        indcStart=page-3 if page>=4 else 1
        pagesCuont=ceil(count/25)
        remPages=ceil((count-fromN)/25)
        if page>pagesCuont and remPages: return redirect(f'/dashboard/advertise-messages/{language}/1')
        pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
       
        contxt={
            'lang':language,
            'requests':requests,
            'pages':pages,
            'currentPage':page

        }
        return render(request,'dashboard/advertiseMessages.html',contxt)
    else:
        return redirect("/dashboard/login")

def deleteAdverticeMessage(request,language,page):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'request-id' in request.POST:
            try:
                theRequest=AdvertistRequest.objects.get(pk=int(request.POST['request-id']))
                theRequest.delete()
                return redirect(f'/dashboard/advertise-messages/{language}/{page}')
            except (AdvertistRequest.DoesNotExist,ValueError):
                return HttpResponse("ID is not valid")
        else:
            return HttpResponse("ID is not valid")

    else:
        return redirect("/dashboard/login")


def showAdverticeMessage(request,messageID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        try:
            theRequest=AdvertistRequest.objects.get(pk=messageID)
            contxt={
                'theRequest':theRequest,
                
            }
            return render(request,'dashboard/advertiseRequest.html',contxt)
        except (AdvertistRequest.DoesNotExist,ValueError):
            return HttpResponse("ID is not valid")
    else:
        return redirect("/dashboard/login")


