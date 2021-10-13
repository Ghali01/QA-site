from content.models import Category,Tag
from django.contrib import messages
from django.shortcuts import render,redirect
from django.urls import reverse
from dashboard.decorators import forSuperAdmin
from feedback.models import SuggestedCategory, SuggestedTag
from math import ceil
@forSuperAdmin
def suggestedCategories(request,page,language):
    categories=SuggestedCategory.objects.filter(language=language)
    page=1 if page==0 else page
    count=len(categories)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(categories): return redirect(reverse('dashboard:questions',kwargs={'page':1}))
    categories=list(categories)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={
        'categories':categories,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'lang':language

    }
    return render(request,'dashboard/suggestedCategories.html',contxt)


@forSuperAdmin
def deleteSuggestedCategory(request):
    if 'page' in request.POST and 'del-id' in request.POST:
        try:
            cate=SuggestedCategory.objects.get(pk=int(request.POST['del-id']))
            cate.delete() 
            messages.success(request,'item was removed')
            return redirect(reverse('dashboard:suggested-categories',kwargs={'language':cate.language,'page':request.POST['page']}))
        except (SuggestedCategory.DoesNotExist,ValueError):
            pass

    return redirect(reverse('dashboard:suggested-categories',kwargs={'language':'en','page':1}))


@forSuperAdmin
def acceptSuggestdCategory(request,itemID,page):
    try:
        cate=SuggestedCategory.objects.get(pk=itemID)
        Category.objects.create(
            name=cate.name,
            description=cate.description,
            parent=cate.parent,
            language=cate.language,
        )
        cate.delete() 
        messages.success(request,'item was accepted')
        
        return redirect(reverse('dashboard:suggested-categories',kwargs={'language':cate.language,'page':page}))
    except (SuggestedCategory.DoesNotExist,ValueError):
        pass

    return redirect(reverse('dashboard:suggested-categories',kwargs={'language':'en','page':page}))

@forSuperAdmin
def acceptCategoryAfterApproval(request):
    if 'item-name' in request.POST and 'item-desc' in request.POST and 'item-id' in request.POST and 'page' in request.POST:
        try:
            cate=SuggestedCategory.objects.get(pk=request.POST['item-id'])
            Category.objects.create(
                name=request.POST['item-name'],
                description=request.POST['item-desc'],
                parent=cate.parent,
                language=cate.language,
            )
            cate.delete() 
            messages.success(request,'item was accepted')
            
            return redirect(reverse('dashboard:suggested-categories',kwargs={'language':cate.language,'page':request.POST['page']}))
        except (SuggestedCategory.DoesNotExist,ValueError):
            pass
    
    return redirect(reverse('dashboard:suggested-categories',kwargs={'language':'en','page':1}))
@forSuperAdmin
def suggestedTags(request,page,language):
    tags=SuggestedTag.objects.filter(category__language=language)
    page=1 if page==0 else page
    count=len(tags)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(tags): return redirect(reverse('dashboard:questions',kwargs={'page':1}))
    tags=list(tags)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={
        'tags':tags,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'lang':language

    }
    return render(request,'dashboard/suggestedTags.html',contxt)


@forSuperAdmin
def deleteSuggestedTag(request):
    if 'page' in request.POST and 'del-id' in request.POST:
        try:
            tag=SuggestedTag.objects.get(pk=int(request.POST['del-id']))
            tag.delete() 
            messages.success(request,'item was removed')
            return redirect(reverse('dashboard:suggested-tags',kwargs={'language':tag.category.language,'page':request.POST['page']}))
        except (SuggestedTag.DoesNotExist,ValueError):
            pass

    return redirect(reverse('dashboard:suggested-tags',kwargs={'language':'en','page':1}))


@forSuperAdmin
def acceptSuggestdTag(request,itemID,page):
    try:
        tag=SuggestedTag.objects.get(pk=itemID)
        Tag.objects.create(
            name=tag.name,
            description=tag.description,
            category=tag.category,
        )
        tag.delete() 
        messages.success(request,'item was accepted')
        
        return redirect(reverse('dashboard:suggested-tags',kwargs={'language':tag.category.language,'page':page}))
    except (SuggestedTag.DoesNotExist,ValueError):
        pass

    return redirect(reverse('dashboard:suggested-tags',kwargs={'language':'en','page':page}))

@forSuperAdmin
def acceptTagAfterApproval(request):
    if 'item-name' in request.POST and 'item-desc' in request.POST and 'item-id' in request.POST and 'page' in request.POST:
        try:
            tag=SuggestedTag.objects.get(pk=request.POST['item-id'])
            Tag.objects.create(
                name=request.POST['item-name'],
                description=request.POST['item-desc'],
                category=tag.category,
            )
            tag.delete() 
            messages.success(request,'item was accepted')
            
            return redirect(reverse('dashboard:suggested-tags',kwargs={'language':tag.category.language,'page':request.POST['page']}))
        except (SuggestedTag.DoesNotExist,ValueError):
            pass
    
    return redirect(reverse('dashboard:suggested-tags',kwargs={'language':'en','page':1}))
