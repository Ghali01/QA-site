from django.shortcuts import get_object_or_404, redirect, render as _render
from django.urls.base import reverse
from authusers.models import AuthList
from interviewsquestions.settings import BASE_DIR, MEDIA_ROOT
from django.http import HttpResponse
from domonic.html import *
from bs4 import BeautifulSoup
from random import randrange
from django.core.files.storage import FileSystemStorage
from misc.models import AdvertiseImage, AdvertisePage, Service,InfoItem
from dashboard.decorators import forSuperAdmin

def genRandomStr():
    '''
        this function genarate id for a card
    '''
    i = 0
    str = ''
    while i <= 20:
        str += chr(randrange(65, 90))
        i += 1
    return str



def editColumnPage(request, language, side):
    '''
        this view render edit columns page (cards page)
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        # get the file
        path = BASE_DIR.joinpath(
            f'templates/columnsCards/{side}_{language}.html')

        cardsData = []
        # collect cards data
        with open(path,encoding='utf-8') as htmlf:
            doc = BeautifulSoup(htmlf, 'html.parser')
            cards = doc.find_all(class_='card')
            for card in cards:
                cardsData.append(
                    {
                        'id': card['id'],
                        'title': str(card.find(class_="card-title").string)
                    }
                )
        contxt = {
            'lang': language,
            'sid': side,
            'cards': cardsData
        }
        return _render(request, 'dashboard/editColumn.html', context=contxt)
    else:
        return redirect("/dashboard/login")


def deleteCard(request, language, side):
    '''
        this view delete a card from grml file
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'card-id' in request.POST:
            path = BASE_DIR.joinpath(
                f'templates/columnsCards/{side}_{language}.html')
            with open(path, 'r+',encoding='utf-8') as htmlf:
                doc = BeautifulSoup(htmlf, 'html.parser')
                doc.select(f'#{request.POST["card-id"]}')[0].decompose() #delete the card
                # save the file
                htmlf.seek(0)
                htmlf.truncate()
                htmlf.write(doc.prettify())
        return redirect(f'/dashboard/column/{language}/{side}')
    else:
        return redirect("/dashboard/login")


def addCardPage(request, language, side):
    '''
        this view render add card page
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:

        contxt = {
            'lang': language,
            'sid': side,
            'isNew': True
        }
        return _render(request, 'dashboard/addEditCard.html', contxt)
    else:
        return redirect("/dashboard/login")


def addCard(request, language, side):
    '''
        this view add a card tho the html file
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'card-title' in request.POST and 'card-body' in request.POST:
            # open the file
            path = BASE_DIR.joinpath(
                f'templates/columnsCards/{side}_{language}.html')
            with open(path, 'r+',encoding='utf-8') as htmlf:
                doc = BeautifulSoup(htmlf, 'html.parser')
                # create the card
                id = genRandomStr()
                card = f'''<div class="card" id="{id}">
                    <div class="card-header">
                        <h5 class="card-title">{request.POST['card-title']}</h5>
                    </div><div class="card-body">{request.POST['card-body']}</div>
                </div>
                
                '''
                doc.find(class_='cards').append(
                    BeautifulSoup(card, 'html.parser'))
                # save the file
                htmlf.seek(0)
                htmlf.truncate()
                htmlf.write(doc.prettify())
        return redirect(f'/dashboard/column/{language}/{side}')
    else:
        return redirect("/dashboard/login")


def editCardPage(request, language, side, cardID):
    '''
        this view render edit card page
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        # open the file
        path = BASE_DIR.joinpath(
            f'templates/columnsCards/{side}_{language}.html')
        # get card data from the files
        cardBody = cardTitle = None
        with open(path,encoding='utf-8') as htmlf:
            doc = BeautifulSoup(htmlf, 'html.parser')
            card = doc.select(f'#{cardID}')[0]
            cardTitle = card.find(class_='card-title').string.strip()
            cardBody = ''
            for ele in card.find(class_='card-body').contents:
                cardBody += str(ele)
        contxt = {
            'lang': language,
            'sid': side,
            'isNew': False,
            'cardId': cardID,
            'cardBody': cardBody,
            'cardTitle': cardTitle
        }
        return _render(request, 'dashboard/addEditCard.html', contxt)
    else:
        return redirect("/dashboard/login")


def updateCard(request, language, side, cardID):
    '''
        this viwe save the changes on card
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'card-title' in request.POST and 'card-body' in request.POST and 'card-id' in request.POST:
            path = BASE_DIR.joinpath(
                f'templates/columnsCards/{side}_{language}.html')
            htmlf = open(path, 'r',encoding='utf-8')
            doc = BeautifulSoup(htmlf, 'html.parser')
            card = doc.select(f'#{cardID}')[0]
            card.find(
                class_="card-title").string.replace_with(request.POST['card-title'])
            cardBody = card.find(class_="card-body")
            cardBody.clear()
            cardBody.append(BeautifulSoup(
                request.POST['card-body'], 'html.parser'))
            htmlf.close()
            htmlf2 = open(path, 'w',encoding='utf-8')
            htmlf2.write(doc.prettify())
            htmlf2.close()
        return redirect(f'/dashboard/edit-card/{language}/{side}/{cardID}')
    else:
        return redirect("/dashboard/login")


def editFooterPage(request, language):

    '''
        this view render edit footer page
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        path = BASE_DIR.joinpath(
            f'templates/utilities/_customFooter{language}.html')
        htmlf = open(path, 'r',encoding='utf-8')
        customHTML = htmlf.read()
        htmlf.close()
        contxt = {
            'customHTML': customHTML,
            'lang': language
        }

        return _render(request, 'dashboard/editFooter.html', contxt)
    else:
        return redirect("/dashboard/login")


def saveFooter(request, language):
    '''
        this view save the footer
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'custom-html' in request.POST:
            path = BASE_DIR.joinpath(
                f'templates/utilities/_customFooter{language}.html')
            htmlf = open(path, 'w',encoding="utf-8")
            htmlf.write(request.POST['custom-html'])
            htmlf.close()

        return redirect('/dashboard/edit-footer/'+language)
    else:
        return redirect("/dashboard/login")


def editHeaderPage(request, language):
    '''
        this viwe render edit header page
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        path = BASE_DIR.joinpath(f'templates/utilities/_brand{language}.html')
        file=open(path,'r',encoding='utf-8')
        title=file.read()
        file.close()
        contxt = {
            'lang': language,
            'title': title,
        }
        return _render(request, 'dashboard/editHeader.html', context=contxt)
    else:
        return redirect("/dashboard/login")


def saveHeader(request, language):
    '''
        this view save the header
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'logo' in request.FILES:
            
            # upload the logo
            logoFile = request.FILES['logo']
            fs = FileSystemStorage(location=MEDIA_ROOT.joinpath('brand'))
            fileName = f'logo{language}.png'
            if fs.exists(fileName):
                fs.delete(fileName)
            fs.save(fileName, logoFile)
        
        if 'favicon' in request.FILES:
            
            # upload the favicon
            
            fs = FileSystemStorage(location=MEDIA_ROOT)
            
            if fs.exists('favicon.ico'):
                fs.delete('favicon.ico')
            fs.save('favicon.ico', request.FILES['favicon'])
        
        # save the title and text
        if 'title' in request.POST:
            path = BASE_DIR.joinpath(
                f'templates/utilities/_brand{language}.html')
            
            file=open(path,'w',encoding='utf-8')
            file.seek(0)
            file.write(request.POST['title'])
            file.close()
            return redirect('/dashboard/edit-header/'+language)
    else:
        return redirect("/dashboard/login")


def editAdvertisePage(request, language):
    '''
        this view render the edit advertise page
    
    '''
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        pageData = None
        try:
            pageData = AdvertisePage.objects.get(language=language)
        except AdvertisePage.DoesNotExist:
            pageData = AdvertisePage.objects.create(language=language)
        contxt = {
            'lang': language,
            'pageData': pageData
        }
        return _render(request, 'dashboard/editAdvertise.html', contxt)
    else:
        return redirect("/dashboard/login")


def saveAdvertise(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        pageData = None
        try:
            pageData = AdvertisePage.objects.get(language=language)
        except AdvertisePage.DoesNotExist:
            pass
        if 'title' in request.POST and 'text' in request.POST:
            if pageData:
                pageData.text = request.POST['text']
                if request.POST['title']:
                    pageData.title = request.POST['title']
                pageData.save()
            else:
                pageData = AdvertisePage.objects.create(
                    language=language, text=request.POST['text'])
        if 'images' in request.FILES:
            for img in dict(request.FILES)['images']:
                advertiseimage = AdvertiseImage(page=pageData)
                fs = FileSystemStorage(
                    location=MEDIA_ROOT.joinpath('advertise'))
                fileName = fs.generate_filename(img.name)
                fs.save(fileName, img)
                advertiseimage.imageFile.name = 'advertise/'+fileName
                advertiseimage.save()
        return redirect('/dashboard/edit-advertise/'+language)
    else:
        return redirect("/dashboard/login")


def deleteAdvertiseImg(request, language, imageID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        try:
            AdvertiseImage.objects.get(pk=imageID).delete()
        except AdvertiseImage.DoesNotExist:
            pass
        return redirect('/dashboard/edit-advertise/'+language)

    else:
        return redirect("/dashboard/login")


def editServicesPage(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        services = Service.objects.filter(language=language)
        contxt = {
            'lang': language,
            'services': services,

        }
        return _render(request, 'dashboard/editMisc/services.html', contxt)
    else:
        return redirect("/dashboard/login")


def addServicePage(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        contxt = {
            'lang': language,
            'isNew': True
        }
        return _render(request, 'dashboard/editMisc/addEditService.html', contxt)

    else:
        return redirect("/dashboard/login")


def addService(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'title' in request.POST and 'text' in request.POST and 'figure' in request.FILES:
            if request.POST['title']:
                service = Service(
                    title=request.POST['title'], text=request.POST['text'], language=language)
                fs = FileSystemStorage(
                    location=MEDIA_ROOT.joinpath('services'))
                fileName = fs.generate_filename(request.FILES['figure'].name)
                fs.save(fileName, request.FILES['figure'])
                service.image.name = 'services/'+fileName
                service.save()
        return redirect('/dashboard/edit-services/'+language)
    else:
        return redirect("/dashboard/login")


def editServicePage(request, serviceID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        service = None
        try:
            service = Service.objects.get(pk=serviceID)
        except Service.DoesNotExist:
            return HttpResponse('invalid ID')
        contxt = {
            'isNew': False,
            'service': service
        }
        return _render(request, 'dashboard/editMisc/addEditService.html', contxt)

    else:
        return redirect("/dashboard/login")


def updateService(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'title' in request.POST and 'text' in request.POST and 'service-id' in request.POST:
            if request.POST['title']:
                try:
                    service = Service.objects.get(
                        pk=int(request.POST['service-id']))
                    service.title = request.POST['title']
                    service.text = request.POST['text']
                    if 'figure' in request.FILES:
                        fs = FileSystemStorage(
                            location=MEDIA_ROOT.joinpath('services'))
                        fileName = fs.generate_filename(
                            request.FILES['figure'].name)
                        fs.delete(service.image.name)
                        fs.save(fileName, request.FILES['figure'])
                        service.image.name = 'services/'+fileName
                    service.save()
                except (Service.DoesNotExist, ValueError):
                    return HttpResponse('invalid ID')
        return redirect('/dashboard/edit-service/'+request.POST['service-id'])
    else:
        return redirect("/dashboard/login")


def deleteService(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'service-id' in request.POST:
            try:
                Service.objects.get(
                    pk=int(request.POST['service-id'])).delete()
            except (Service.DoesNotExist, ValueError):
                return HttpResponse('invalid ID')
        return redirect('/dashboard/edit-services/'+language)

    else:
        return redirect("/dashboard/login")
# 


def editInfoPage(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        items = InfoItem.objects.filter(language=language)
        contxt = {
            'lang': language,
            'items': items,

        }
        return _render(request, 'dashboard/editMisc/editInfo.html', contxt)
    else:
        return redirect("/dashboard/login")


def addInfoItemPage(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        contxt = {
            'lang': language,
            'isNew': True
        }
        return _render(request, 'dashboard/editMisc/addEditInfoItem.html', contxt)

    else:
        return redirect("/dashboard/login")


def addInfoItem(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'title' in request.POST and 'text' in request.POST:
            if request.POST['title']:
                InfoItem.objects.create(
                    title=request.POST['title'],
                    text=request.POST['text'],
                    language=language
                )
        return redirect(reverse('dashboard:edit-info-page',kwargs={'language':language}))
    else:
        return redirect("/dashboard/login")


def editInfoItemPage(request, itemID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        item = None
        try:
            item = InfoItem.objects.get(pk=itemID)
        except InfoItem.DoesNotExist:
            return HttpResponse('invalid ID')
        contxt = {
            'isNew': False,
            'item': item
        }
        return _render(request, 'dashboard/editMisc/addEditInfoItem.html', contxt)

    else:
        return redirect("/dashboard/login")


def updateInfoItem(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'title' in request.POST and 'text' in request.POST and 'item-id' in request.POST:
            if request.POST['title']:
                try:
                    item = InfoItem.objects.get(
                        pk=int(request.POST['item-id']))
                    item.title = request.POST['title']
                    item.text = request.POST['text']
                  
                    item.save()
                except (InfoItem.DoesNotExist, ValueError):
                    return HttpResponse('invalid ID')
        return redirect(reverse('dashboard:edit-info-item-page',kwargs={'itemID':request.POST['item-id']}))
    else:
        return redirect("/dashboard/login")


def deleteInfoItem(request, language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'item-id' in request.POST:
            try:
                InfoItem.objects.get(
                    pk=int(request.POST['item-id'])).delete()
            except (InfoItem.DoesNotExist, ValueError):
                return HttpResponse('invalid ID')
        return redirect(reverse('dashboard:edit-info-page',kwargs={'language':language}))

    else:
        return redirect("/dashboard/login")


@forSuperAdmin
def editAuthPage(request,page,language):
    List=get_object_or_404(AuthList,page=page,language=language)
    if request.method=='POST':
        if 'title' in request.POST and 'items' in request.POST:
            List.title=request.POST['title']
            List.list=request.POST['items']
            List.save()
            return redirect(reverse('dashboard:edit-auth-page',kwargs={'page':page,'language':language}))
    contxt={
        'list':List
    }
    return _render(request,'dashboard/editAuthPage.html',contxt)