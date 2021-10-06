from json.decoder import JSONDecodeError
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.utils.translation import get_language
from content.models import Category,Tag
from dashboard.decorators import forSuperAdmin
from polls.models import Poll,PollItem,PollResault
import json
from math import ceil
@forSuperAdmin
def polls(request,page,language):
    polls=Poll.objects.filter(language=language)
    polls=list(polls)
    page=1 if page==0 else page
    count=len(polls)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    # if page>pagesCuont and remPages and len(polls): return redirect(reverse('dashboard:questions',kwargs={'page':1}))
    polls=list(polls)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    
    contxt={
        'polls':polls,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
     'lang':language
    }
    return render(request,'dashboard/pollsManagement.html',contxt)

@forSuperAdmin
def addPoll(request,language):
    
    categories=Category.objects.filter(parent=None,language=language)
    tags=Tag.objects.filter(category__language=language)
    if request.method=='POST':
        if 'title' in request.POST and 'text' in request.POST and 'categories' in request.POST and 'tags' in request.POST and 'poll-items' in request.POST  and request.POST['title']:
            try:
                poll=Poll(
                    title=request.POST['title'],
                    text=request.POST['text'],
                    language=language,
                    isPublished='published' in request.POST,
                    isOpened='published' in request.POST,
                )
                poll.save()
                tagsIds=json.loads(request.POST['tags'])
                for tagId in tagsIds:
                    poll.tags.add(tags.get(pk=int(tagId)))
                categoriesIds=json.loads(request.POST['categories'])
                for categoryId in categoriesIds:
                    if not int(categoryId)==0:
                        poll.categories.add(Category.objects.get(pk=int(categoryId)))
                items=json.loads(request.POST['poll-items'])
                for item in items:
                    opts=[]
                    for opt in item['options']:
                        if not opt in opts:
                            opts.append(opt)
                    PollItem.objects.create(
                        text=item['text'],
                        type=item['type'],
                        options=json.dumps(opts),
                        poll=poll
                    )
                messages.success(request,'poll Added')
                return redirect(reverse('dashboard:polls',kwargs={'language':language,'page':1}))
            except (JSONDecodeError,ValueError,Tag.DoesNotExist,Category.DoesNotExist):
                pass
    contxt={
        'categories':categories,
        'tags':tags,
        'isNew':True

    }
    return render(request,'dashboard/addEditPoll.html',contxt)

@forSuperAdmin
def deletePoll(request):
    if 'del-id' in request.POST and 'page' in request.POST  and request.POST['del-id'].isnumeric():
        poll= get_object_or_404(Poll,id=int(request.POST['del-id']))
        poll.delete()
        messages.success(request,'poll removed')
        return redirect(reverse('dashboard:polls',kwargs={'language':poll.language,'page':request.POST['page']}))

    return redirect(reverse('dashboard:polls',kwargs={'language':'en','page':1}))
    

@forSuperAdmin
def editPoll(request,pollID):
    poll=get_object_or_404(Poll,id=pollID)
    categories=Category.objects.filter(parent=None,language=poll.language)
    tags=Tag.objects.filter(category__language=poll.language)
    if request.method=='POST':
        if 'title' in request.POST and 'text' in request.POST and 'categories' in request.POST and 'tags' in request.POST and 'poll-items' in request.POST  and request.POST['title']:
            try:
                poll.title=request.POST['title']
                poll.text=request.POST['text']
                isPub=poll.isPublished
                if not isPub:
                    poll.isPublished='published' in request.POST
                    poll.isOpened='published' in request.POST
                poll.save()
                poll.tags.clear()
                tagsIds=json.loads(request.POST['tags'])
                for tagId in tagsIds:
                    poll.tags.add(tags.get(pk=int(tagId)))
                poll.categories.clear()
                categoriesIds=json.loads(request.POST['categories'])
                for categoryId in categoriesIds:
                    if not int(categoryId)==0:
                        poll.categories.add(Category.objects.get(pk=int(categoryId)))
                items=json.loads(request.POST['poll-items'])
                if not isPub:
                    poll.items.all().delete()
                    for item in items:
                        
                        opts=[]
                        for opt in item['options']:
                            if not opt in opts:
                                opts.append(opt)
                        PollItem.objects.create(
                            text=item['text'],
                            type=item['type'],
                            options=json.dumps(opts),
                            poll=poll
                        )
            except (JSONDecodeError,ValueError,Tag.DoesNotExist,Category.DoesNotExist):
                pass

    contxt={
        'poll':poll,
        'isNew':False,
        'categories':categories,
        'tags':tags,
    }
    return render(request,'dashboard/addEditPoll.html',contxt)

@forSuperAdmin
def publishPoll(request):
    if 'poll-id' in request.POST:
        try:
            poll=Poll.objects.get(id=int(request.POST['poll-id']))
            poll.isOpened=True
            poll.isPublished=True
            poll.save()
            return HttpResponse('done')
        except(ValueError,Poll.DoesNotExist):
            pass
    return HttpResponse('erorr')
@forSuperAdmin
def toggPollOpen(request):
    if 'poll-id' in request.POST:
        try:
            
            poll=Poll.objects.get(pk=int(request.POST['poll-id']))
            if not poll.isOpened:
                poll.isOpened=True
                poll.isPublished=True
                poll.save()
                return HttpResponse('opened')
            else:
                poll.isOpened=False
                poll.save()
                return HttpResponse('closed')

        except(Poll.DoesNotExist,ValueError):
            pass

    return HttpResponse('error')

@forSuperAdmin
def pollResault(request,pollID):
    poll=get_object_or_404(Poll,id=pollID)
    contxt={
        'poll':poll
    }
    return render(request,'dashboard/pollResaults.html',contxt)