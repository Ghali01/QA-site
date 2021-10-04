from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from content.models import Category,Tag
from dashboard.decorators import forSuperAdmin
from polls.models import Poll,PollItem

@forSuperAdmin
def polls(request,language):
    contxt={
        'lang':language
    }
    return render(request,'polls/pollsManagement.html',contxt)

@forSuperAdmin
def addPoll(request,language):
    categories=Category.objects.filter(parent=None,language=language)
    tags=Tag.objects.filter(category__language=language)
    contxt={
        'categories':categories,
        'tags':tags
    }
    return render(request,'polls/addPoll.html',contxt)