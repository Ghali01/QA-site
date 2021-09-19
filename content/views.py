from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser, forModerator,userHasTags
from content.models import Category, PostLog,Tag,SuggestedQuestion,Post,Question, Voter,Answer
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models.expressions import F
import json
@forActiveUser
@userHasTags
def index(request,categoryID=-1):
    if request.user.is_authenticated and not request.user.is_anonymous:
        tagsFilter=viewsFilter=votesFilter=answeileter=None
        category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
        questions=Question.objects.all()
        if category:
            questions=questions.filter(category=category)
                
        if 'tags' in request.GET and request.GET['tags']=='M':
            tagsFilter=request.GET['tags']
            for tag in request.user.profile.tags.all():
                questions=questions.filter(tags=tag)
        if category:
               questions=questions.union(*subCategoryQuestions(category,request))
        questions=questions[:20]  
        contxt={
            'category':category,
            'questions':questions
        }
        return render(request,'content/index.html',contxt)
    else:
        return redirect(reverse('login-page'))


def subCategoryQuestions(category,request):
    sets=[]
    for subCate in category.getAllSubCategories():
        questions=Question.objects.filter(category=subCate)

        if 'tags' in request.GET and request.GET['tags']=='M':
            tagsFilter=request.GET['tags']
            for tag in request.user.profile.tags.all():
                questions=questions.filter(tags=tag)
        sets.append(questions)
    return sets
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


def questionPage(request,questionID):
    question=get_object_or_404(Question,id=questionID)
    question.views=F('views')+1
    question.save()
    question.refresh_from_db()
    contxt={
        'question':question
    }
    return render(request,'content/questionPage.html',contxt)

@forActiveUser
def postVotes(request):

    if 'type' in request.GET and 'post-id' in request.GET:
        type=request.GET['type']
        
        post=Post.objects.get(pk=int(request.GET['post-id']))
        if type=='up':
            if not Voter.objects.filter(user=request.user,post_id=request.GET['post-id'],type=Voter.types.Up).exists():
                Voter.objects.create(user=request.user,post=post,type=Voter.types.Up)
                try:
                    v=Voter.objects.get(user=request.user,post=post,type=Voter.types.Down)
                    v.delete()
                    post.votes=F('votes')+2
                except  Voter.DoesNotExist:
                    post.votes=F('votes')+1
                post.save()
                post.refresh_from_db()
                
                return HttpResponse(json.dumps({'resault':'done','votes':post.getVotes()}))
            else:
                return HttpResponse(json.dumps({'resault':'alradey Voted'}))

        elif type=='down':
            if not Voter.objects.filter(user=request.user,post_id=request.GET['post-id'],type=Voter.types.Down).exists():
                Voter.objects.create(user=request.user,post=post,type=Voter.types.Down)
                try:
                    v=Voter.objects.get(user=request.user,post=post,type=Voter.types.Up)
                    v.delete()
                    post.votes=F('votes')-2
                except  Voter.DoesNotExist:
                    post.votes=F('votes')-1
                post.save()
                post.refresh_from_db()

                return HttpResponse(json.dumps({'resault':'done','votes':post.getVotes()}))
            else:
                return HttpResponse(json.dumps({'resault':'alradey Voted'}))
    return HttpResponse(json.dumps({'resault':'error'}))

@forActiveUser
def addAnswer(request):
    if 'que-id' in request.POST and 'ans-text' in request.POST: 
        try:
            question=get_object_or_404(Question,id=int(request.POST['que-id'])) 
            post=Post.objects.create(text=request.POST['ans-text'],author=request.user,type=Post.types.Answer)
            log=PostLog.objects.create(post=post,text=request.POST['ans-text'],author=request.user,type=PostLog.types.Suggest)
            answer=Answer.objects.create(post=post,question=question)
            messages.success(request,'The answer has been submitted, it will be reviewed soon.')
            return redirect(reverse('content:question-page',kwargs={'questionID':request.POST['que-id']})+'#mgss')
        except ValueError:
            pass
    return redirect(reverse('content:index'))