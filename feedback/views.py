from django.shortcuts import render,redirect
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,userHasTags
from content.models import Category
from django.utils.translation import get_language
from .models import SuggestedCategory,SuggestedTag
from django.contrib import messages
@forActiveUser
@userHasTags
def suggestCategory(request):
    if request.method=='POST':
        if 'cate-name' in request.POST and 'cate-desc' in request.POST and 'category-id' in request.POST:
            currentLanguage =get_language()[:2]
            try:
                SuggestedCategory.objects.create(
                    suggester=request.user,
                    name=request.POST['cate-name'],
                    description=request.POST['cate-desc'],
                    language=currentLanguage,
                    parent=Category.objects.get(pk=int(request.POST['category-id']))
                )
            except (Category.DoesNotExist,ValueError):
                pass
            messages.success(request,'Your suggest has been submited')
    categories=Category.objects.filter(parent=None)
    contxt={
        'categories':categories
    }
    return render(request,'feedback/suggestCategory.html',contxt)

@forActiveUser
@userHasTags
def suggestTag(request):
    if request.method=='POST':
        if 'tag-name' in request.POST and 'tag-desc' in request.POST and 'category-id' in request.POST:
            currentLanguage =get_language()[:2]
            try:
                SuggestedTag.objects.create(
                    suggester=request.user,
                    name=request.POST['tag-name'],
                    description=request.POST['tag-desc'],
                    category=Category.objects.get(pk=int(request.POST['category-id']))
                )
            except (Category.DoesNotExist,ValueError):
                pass
            messages.success(request,'Your suggest has been submited')
    categories=Category.objects.filter(parent=None)
    contxt={
        'categories':categories
    }
    return render(request,'feedback/suggestTag.html',contxt)

