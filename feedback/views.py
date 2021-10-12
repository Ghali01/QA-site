from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,userHasTags
from content.models import Category, Post
from django.utils.translation import get_language
from .models import FlagReason, SuggestedCategory,SuggestedTag,Reports
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

@forActiveUser
def report(request):
    if 'type' in request.POST and 'report-on' in request.POST and 'reason' in request.POST:
        if request.POST['type']=='Q' or  request.POST['type']=='A':
            post=get_object_or_404(Post,id=int(request.POST['report-on']))
            Reports.objects.create(
                post=post,
                reason=get_object_or_404(FlagReason,id=int(request.POST['reason'])),
                reporter=request.user,
                
            )
            return redirect(reverse('content:question-page',kwargs={'questionID':post.getQuestion().id}))
        elif request.POST['type']=='U':
            user=get_object_or_404(User,id=int(request.POST['report-on']))
            Reports.objects.create(
                user=user,
                reason=get_object_or_404(FlagReason,id=int(request.POST['reason'])),
                reporter=request.user,
                
            )
            return redirect(reverse('profiles:profile-page',kwargs={'userID':user.id}))

    return redirect(reverse('content:index'))