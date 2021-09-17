import datetime
from json.decoder import JSONDecodeError
from math import ceil
from typing_extensions import ParamSpec
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser, forModerator,userHasTags
from content.models import Category, PostLog,Tag,SuggestedQuestion,Post,Question, Voter,Answer,Comment
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models.expressions import F,Q
from django.db.models import Count
from django.template.loader import render_to_string
import json
@forActiveUser
@userHasTags
def index(request,categoryID=-1):
    if request.user.is_authenticated and not request.user.is_anonymous:
        tagsFilter=viewsFilter=votesFilter=answersFilter=None
        category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
        questions=Question.objects.all()
        if category:
            questions=questions.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category))
        if 'time' in request.GET:
            if request.GET['time']=='T':
                logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date=datetime.datetime.now().date())
                questions=questions.filter(post__logs__in=logs)
            elif request.GET['time']=='W':
                logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date__range=(datetime.datetime.now().date()-datetime.timedelta(days=7),datetime.datetime.now().date()))
                questions=questions.filter(post__logs__in=logs)
            elif request.GET['time']=='M':               
                logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date__range=(datetime.datetime.now().date()-datetime.timedelta(days=30),datetime.datetime.now().date()))
                questions=questions.filter(post__logs__in=logs)
            
        if 'tags' in request.GET and request.GET['tags']=='M':
            tagsFilter=request.GET['tags']
            for tag in request.user.profile.tags.all():
                questions=questions.filter(tags=tag)

        questions=questions.annotate(Count(F('answers')))
        orderFields=[
            '-post__ActiveDate',
            ('-post__votes' if request.GET['votes']=='M' else 'post__votes') if 'votes' in request.GET else None,
            ('-views' if request.GET['views']=='M' else 'views') if 'views' in request.GET else None,
            ('-answers__count' if request.GET['answers']=='M' else 'answers__count') if 'answers' in request.GET else None,

        ]
        orderFields=list(filter(lambda it: not it == None ,orderFields))
        questions=questions.order_by(*orderFields)
        if 'votes' in request.GET:
            votesFilter=request.GET['votes']
        if 'views' in request.GET:
            viewsFilter=request.GET['views']
        if 'answers' in request.GET:
            answersFilter=request.GET['answers']
        pageCount=ceil(questions.count()/15)  
        questions=questions[:15]
        contxt={
            'category':category,
            'questions':questions,
            'votesFilter':votesFilter,
            'viewsFilter':viewsFilter,
            'answersFilter':answersFilter,
            'tagsFilter':tagsFilter,
            'categoryID':categoryID if not categoryID==-1 else None,
            'pageCount':pageCount
        }
        return render(request,'content/index.html',contxt)
    else:
        return redirect(reverse('login-page'))

def seeMoreQueIndex(request,page,categoryID=-1):
     if request.user.is_authenticated and not request.user.is_anonymous:
        category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
        questions=Question.objects.all()
        if category:
            questions=questions.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category))
        if 'time' in request.GET:
            if request.GET['time']=='T':
                logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date=datetime.datetime.now().date())
                questions=questions.filter(post__logs__in=logs)
            elif request.GET['time']=='W':
                logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date__range=(datetime.datetime.now().date()-datetime.timedelta(days=7),datetime.datetime.now().date()))
                questions=questions.filter(post__logs__in=logs)
            elif request.GET['time']=='M':
               
                logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date__range=(datetime.datetime.now().date()-datetime.timedelta(days=30),datetime.datetime.now().date()))
                questions=questions.filter(post__logs__in=logs)
            
        if 'tags' in request.GET and request.GET['tags']=='M':
            tagsFilter=request.GET['tags']
            for tag in request.user.profile.tags.all():
                questions=questions.filter(tags=tag)
        questions=questions.annotate(Count(F('answers')))
        
        orderFields=[

            '-post__ActiveDate',
            ('-post__votes' if request.GET['votes']=='M' else 'post__votes') if 'votes' in request.GET else None,
            ('-views' if request.GET['views']=='M' else 'views') if 'views' in request.GET else None,
            ('-answers__count' if request.GET['answers']=='M' else 'answers__count') if 'answers' in request.GET else None,

        ]
        orderFields=list(filter(lambda it: not it == None ,orderFields))
        questions=questions.order_by(*orderFields)

        remPages=int(ceil(questions.count()/15)-page-1)
        questions=questions[page*15:(page*15)+15]

        htmlStr=''
        for que in questions:
            htmlStr+= render_to_string('content/templatetags/questionitem.html',{'question':que})
        return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))
        
@forActiveUser
@userHasTags
def addQuestionPage(request):
    if request.method == 'POST':
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
                    if tagsIds:
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
                selectedTags=[]
                if tagsIds:
                    for tagID in tagsIds:
                        selectedTags.append(Tag.objects.get(pk=tagID))
                category=Category.objects.get(pk=request.POST['category-id'])          
                categories=Category.objects.filter(parent=None)
                tags=Tag.objects.all()
                contxt={
                    'questionTitle':request.POST['post-title'],
                    'questionBody':request.POST['post-body'],
                    'selectedTags':selectedTags,
                    'category':category,
                    'categories':categories,
                    'tags':tags
        
                }           
                return render(request,'content/addQuestion.html',context=contxt)

        return redirect(reverse('content:add-question'))

    else:
        categories=Category.objects.filter(parent=None)
        tags=Tag.objects.all()
        contxt={
            'categories':categories,
            'tags':tags
        }
        return render(request,'content/addQuestion.html',context=contxt)


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

def similarQuestions(request,page):
    if 'que-title' in request.GET and 'category-id' in request.GET and 'tags' in request.GET:
        try:
            category=int(request.GET['category-id'])

            questions=Question.objects.filter(Q(category__id=category)|Q(category__parent__id=category)|Q(category__parent__parent__id=category)|Q(category__parent__parent__parent__id=category))
            tagsIds=json.loads(request.GET['tags'])
            for tagId in tagsIds:
                questions=questions.filter(tags__id=tagId)
            questions=questions.filter(title__contains=request.GET['que-title'])            
        
            remPages=int(ceil(questions.count()/15)-page-1)
            questions=questions[page*15:(page*15)+15]
            
            htmlStr=''
            for que in questions:
                htmlStr+= render_to_string('content/templatetags/questionitem.html',{'question':que})
            return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))
            


        except (ValueError,JSONDecodeError):
            pass

    return HttpResponse('value Error')

@forActiveUser
@userHasTags
def addCommentToPost(requset):
    if 'post-id' in requset.POST and 'text' in requset.POST:
        if requset.POST['text']:
            # try:
                comment=Comment.objects.create( text=requset.POST['text'],
                                                post=Post.objects.get(pk=int(requset.POST['post-id'])),
                                                author=requset.user    
                                                )
                contxt={
                    'comment':comment
                }
                html=render_to_string('content/templatetags/commentItem.html',contxt)
                return HttpResponse(html)
            # except(ValueError,Post.DoesNotExist):
            #     pass

    return HttpResponse('error')

def allPostComment(request):
    if 'post-id' in request.GET:
        try:
            comments=Comment.objects.filter(post_id=int(request.GET['post-id']))
            htmlstr=''
            for comment in comments:
                contxt={
                    'comment':comment
                }
                htmlstr+=render_to_string('content/templatetags/commentItem.html',contxt)
            return HttpResponse(htmlstr)
        except ValueError:
            pass
    return HttpResponse('error')
    