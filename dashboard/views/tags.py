from typing_extensions import TypeGuard
from django.contrib import messages
from django.shortcuts import render,redirect
from django.urls import reverse
from content.models import Category, Tag
from django.http import HttpResponse
import json


def tagsPage(request,language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        categories=Category.objects.filter(language=language,parent=None)
        contxt={
            'lang':language,
            'categories':categories

        }
        return render(request,'dashboard/tags.html',contxt)

    else:
        return redirect(reverse('dashboard:login'))


def addTag(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'cate-id' in request.POST and 'tag-name' in request.POST and 'tag-desc' in request.POST:
            if request.POST['tag-name'] and request.POST['tag-desc']:
                try:
                    category=Category.objects.get(pk=int(request.POST['cate-id']))
                    Tag.objects.create(
                        name=request.POST['tag-name'],
                        description=request.POST['tag-desc'],
                        category=category
                    )
                    messages.success(request,'Tag Created')
                    return redirect(reverse('dashboard:tags',kwargs={'language':category.language}))
                except (Category.DoesNotExist,ValueError):
                    messages.error(request,'invalid id')
            elif not request.POST['tag-name']:
                messages.error(request,'name can not be empty')
            elif not request.POST['tag-desc']:
                messages.error(request,'description can not be empty')
        else:
            messages.error(request,'values error')            
        return redirect(reverse('dashboard:tags',kwargs={'language':category.language}))

    else:
        return redirect(reverse('dashboard:login'))


def tagsCategoryJson(request):
    if 'cate-id' in request.GET:
        try:
            tags=Tag.objects.filter(category=Category.objects.get(pk=request.GET['cate-id']))
            data=[]
            for tag in tags:
                data.append({
                    'name':tag.name,
                    'description':tag.description,
                    'id':tag.id
                })
            return HttpResponse(json.dumps(data))
        except (Category.DoesNotExist,ValueError):
            return HttpResponse('invalid id')
    else:
        return HttpResponse('value error')

def tagsSearchJson(request):
    if 'search-text' in request.GET and 'cate-id' in request.GET:
        tags=Tag.objects.filter(name__contains=request.GET['search-text'],category=Category.objects.get(pk=request.GET['cate-id']))
        data=[]
        for tag in tags:
            data.append({
                'name':tag.name,
                'description':tag.description,
                'id':tag.id
            })
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('value error')

def editTag(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'tag-id' in request.POST and 'tag-name' in request.POST and 'tag-desc' in request.POST:
            try:
                
                tag=Tag.objects.get(pk=int(request.POST['tag-id']))
                tag.name=request.POST['tag-name']
                tag.description=request.POST['tag-desc']
                tag.save()
                return redirect(reverse('dashboard:tags',kwargs={'language':tag.category.language}))
            except(Tag.DoesNotExist,ValueError):
                messages.error(request,'invalid id')

        else:
            messages.error(request,'values error')
        return redirect(reverse('dashboard:tags',kwargs={'language':'en'}))

    else:
        return HttpResponse('value error')

def deleteTag(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'tag-id' in request.POST:
            try:
                tag=Tag.objects.get(pk=int(request.POST['tag-id']))
                tag.delete()
                return redirect(reverse('dashboard:tags',kwargs={'language':tag.category.language}))
            except(Tag.DoesNotExist,ValueError):
                messages.error(request,'invalid id')

        else:
            messages.error(request,'values error')
        return redirect(reverse('dashboard:tags',kwargs={'language':'en'}))

    else:
        return HttpResponse('value error')
