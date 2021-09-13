from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser, forModerator,userHasTags
from content.models import Category, PostLog,Tag,SuggestedQuestion,Post
from django.shortcuts import get_object_or_404
from django.contrib import messages
import json
@forActiveUser
@userHasTags
def index(request,categoryID=-1):
    if request.user.is_authenticated and not request.user.is_anonymous:
        category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
        contxt={
            'category':category
        }
        return render(request,'content/index.html',contxt)
    else:
        return redirect(reverse('login-page'))

@forActiveUser
@userHasTags
def addQuestionPage(request):
    categories=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    contxt={
        'categories':categories,
        'tags':tags
    }
    return render(request,'content/addQuestion.html',context=contxt)

@forActiveUser
def addQuestion(request):
    if 'post-title' in request.POST and 'post-body' in request.POST and 'category-id' in request.POST and 'tags' in request.POST:
        tagsIds=None
        try:
            tagsIds=json.loads(request.POST['tags'])
        except :
            pass
        if request.POST['post-title'] and request.POST['post-body'] and tagsIds:
            try:
                post=Post.objects.create(text=request.POST['post-body'],author=request.user,type=Post.types.Question)
                question=SuggestedQuestion(title=request.POST['post-title'],post=post,
                category=Category.objects.get(pk=request.POST['category-id']))
                question.save()
                tags=[] 
                for tagID in tagsIds:
                    tags.append(Tag.objects.get(pk=tagID))
                question.tags.add(*tags)
                question.save()
                PostLog.objects.create(post=post,text=post.text,title=question.title,author=request.user,type=PostLog.types.Suggest)
                messages.success(request,'The question has been submitted, it will be reviewed soon.')
                return redirect(reverse('content:index'))

            except Category.DoesNotExist:
                messages.error(request,'Category Not found')
        else:
            if not request.POST['post-title']:
                messages.error(request,'Title should not be empty' ,extra_tags='title')
            if not request.POST['post-body']:
                messages.error(request,'Question Text should not be empty',extra_tags='body')
            if not tagsIds:
                messages.error(request,'You most add 1 tag or more',extra_tags='tags')
    return redirect(reverse('content:add-question'))


