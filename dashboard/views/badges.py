
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from dashboard.decorators import forSuperAdmin
from content.models import Badge,Category,Tag
from django.contrib import messages
from math import ceil
import json

@forSuperAdmin
def BadgesPage(request,page):
    categories=Category.objects.all()
    tags=Tag.objects.all()
    badges= Badge.objects.all()
    lvl=reason=targetStr=None
    search=''
    if 'search' in request.GET and request.GET['search']:
        search=request.GET['search']
        badges=badges.filter(name__contains=request.GET['search'])

    if 'lvl' in request.GET and not request.GET['lvl']=='0':
        lvl=request.GET['lvl']
        badges=badges.filter(level=request.GET['lvl'])
   
    if 'reason' in request.GET and not request.GET['reason']=='0':
        reason=request.GET['reason']
        badges=badges.filter(reason=request.GET['reason'])
   
    if 'target' in request.GET and not request.GET['target']=='0':
        targetStr=request.GET['target']
        if targetStr.startswith('G'):
            badges=badges.filter(targetType=Badge.targetTypes.General)
        if targetStr.startswith('C'):
            badges=badges.filter(category_id=int(targetStr[1:]))
        if targetStr.startswith('T'):
            badges=badges.filter(tag_id=int(targetStr[1:]))
   
    page=1 if page==0 else page
    count=len(badges)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(badges): return redirect(reverse('dashboard:badges-page',kwargs={'page':1}))
    badges=list(badges)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )


    contxt={
        'badges':badges,
        'categories':categories,
        'tags':tags,
        'currentPage':page,
        'pages':pages ,#if len(pages)>1 else [],
        'search':search,
        'reason':reason,
        'lvl':lvl,
        'targetStr':targetStr
    }

    return render(request,'dashboard/badges.html',contxt)


@forSuperAdmin
def addBadge(request):
    if request.method=='POST':
        if 'name' in request.POST and 'desc' in request.POST and 'lvl' in request.POST and 'reason' in request.POST and  'target-type' in request.POST  and 'count' in request.POST:
            if request.POST['name'] and request.POST['desc']:
                badge=Badge()
                badge.level=request.POST['lvl']
                badge.name=request.POST['name']
                badge.description=request.POST['desc']
                badge.count=request.POST['count']
                badge.reason=request.POST['reason']
                badge.targetType=request.POST['target-type']
                if badge.targetType==Badge.targetTypes.Category:
                    badge.category=Category.objects.get(pk=int(request.POST['target-id']))
                elif badge.targetType==Badge.targetTypes.Tag:
                    badge.tag=Tag.objects.get(pk=int(request.POST['target-id']))
                badge.save()
                messages.success(request,gettext('badge created'))
                return redirect(reverse('dashboard:badges-page',kwargs={'page':1}))
            else:
                messages.error(request,gettext('check empty fields'))
    categories=Category.objects.all()
    tags=Tag.objects.all()
    categoriesJson=[]
    tagsJson=[]
    for cate in categories:
        categoriesJson.append({
            'name':cate.name,
            'id':cate.id
        })
    categoriesJson=json.dumps(categoriesJson)
    for tag in tags:
        tagsJson.append({
            'name':tag.name,
            'id':tag.id
        })
    tagsJson=json.dumps(tagsJson)
    contxt={
        'categories':categories,
        'categoriesJson':categoriesJson,
        'tags':tags,
        'tagsJson':tagsJson,
        'isNew':True
    }
    return render(request,'dashboard/addEditBadge.html',contxt)

@forSuperAdmin
def deleteBadge(request):
    if 'del-id' in request.POST and 'page' in request.POST:
        try:
            Badge.objects.get(pk=request.POST['del-id']).delete()
            messages.success(request,gettext('Badge Removed'))
            return redirect(reverse('dashboard:badges-page',kwargs={'page':request.POST['page']}))

        except(Badge.DoesNotExist,ValueError):
            pass
    
    return redirect(reverse('dashboard:badges-page',kwargs={'page':1}))
    

@forSuperAdmin
def editBadge(request,badgeID):
    badge=get_object_or_404(Badge,id=badgeID)
    if request.method=='POST':
        if 'name' in request.POST and 'desc' in request.POST and 'lvl' in request.POST and 'reason' in request.POST and  'target-type' in request.POST  and 'count' in request.POST:
            if request.POST['name'] and request.POST['desc']:
                badge.name=request.POST['name']
                badge.level=request.POST['lvl']
                badge.description=request.POST['desc']
                badge.count=request.POST['count']
                badge.reason=request.POST['reason']
                badge.targetType=request.POST['target-type']
                if badge.targetType==Badge.targetTypes.Category:
                    badge.category=Category.objects.get(pk=int(request.POST['target-id']))
                    badge.tag=None
                elif badge.targetType==Badge.targetTypes.Tag:
                    badge.tag=Tag.objects.get(pk=int(request.POST['target-id']))
                    badge.category=None
                badge.save()
            else:
                messages.error(request,gettext('check empty fields'))

    categories=Category.objects.all()
    tags=Tag.objects.all()
    categoriesJson=[]
    tagsJson=[]
    for cate in categories:
        categoriesJson.append({
            'name':cate.name,
            'id':cate.id
        })
    categoriesJson=json.dumps(categoriesJson)
    for tag in tags:
        tagsJson.append({
            'name':tag.name,
            'id':tag.id
        })
    tagsJson=json.dumps(tagsJson)
    contxt={
        'categories':categories,
        'categoriesJson':categoriesJson,
        'tagsJson':tagsJson,
        'tags':tags,
        'isNew':False,
        'badge':badge
    }
    return render(request,'dashboard/addEditBadge.html',contxt)
