
from json.decoder import JSONDecodeError
from django.db import models

from django.db.models.query_utils import Q
from django.db.models import F,Func,Count
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,forModerator
from content.models import Answer, Category, Post, PostLog, Question,Tag,SuggestedQuestion
import json
from math import ceil
from django.shortcuts import get_object_or_404
@forActiveUser
@forModerator
def suggestedQuestionsAwait(request,page,mode):
    categoires=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    category=searchVal=order=None
    tagsF=[]
    questions=SuggestedQuestion.objects.all()
    if  mode==PostLog.types.Suggest:
            questions=questions.exclude(
            post__logs__type=PostLog.types.Accept
        ).exclude(
            post__logs__type=PostLog.types.Reject

        )
    elif mode==PostLog.types.Accept:
           questions=questions.filter(
            post__logs__type=PostLog.types.Accept
        )
    elif mode==PostLog.types.Reject:
          questions=questions.filter(
            post__logs__type=PostLog.types.Reject
        ).exclude(
            post__logs__type=PostLog.types.Accept

        )
    if 'category' in request.GET and request.GET['category']:
        try:
            category=Category.objects.get(pk=request.GET['category'])
            questions=questions.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category))

        except Category.DoesNotExist:
            pass
    if 'search' in request.GET and request.GET['search']:
        questions=questions.filter(Q(title__contains=request.GET['search'])  | Q(post__text__contains=request.GET['search']))
        searchVal=request.GET['search']
    if 'tags' in request.GET:
        try:
            tagsIDs=json.loads(request.GET['tags'])
            for tagID in tagsIDs:
                try:    
                    tag=Tag.objects.get(pk=tagID)
                    questions = questions.filter(tags=tag)
                    tagsF.append(tag)
                except Tag.DoesNotExist:
                    pass
        except JSONDecodeError:
            pass
  
  
    if 'order' in request.GET:
        order=request.GET['order']
    if  mode==PostLog.types.Suggest:
        questions=SuggestedQuestion.orderBySuggestDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    if  mode==PostLog.types.Accept:
        questions=SuggestedQuestion.orderByAcceptDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    if  mode==PostLog.types.Reject:
        questions=SuggestedQuestion.orderByRejectDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    questions=list(questions)
    page=1 if page==0 else page
    count=len(questions)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(questions): return redirect(reverse('moderators:suggested-questions-await',kwargs={'page':1}))
    questions=list(questions)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={
        'categories':categoires,
        'tags':tags,
        'questions':questions,
        'category':category,
        'searchVal':searchVal,
        'tagsF':tagsF,
        'order':order,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'mode':mode
    }
    return render(request,'moderators/questions/questions.html',contxt)



@forActiveUser
@forModerator
def reviewQuestionPage(request,questionID):
    question=get_object_or_404(SuggestedQuestion,id=questionID)
    contxt={
        'question':question
    }
    return render(request,'moderators/questions/reviewQuestion.html',context=contxt)
    

@forActiveUser
@forModerator
def changeSuggestQuestion(request):
    if 'que-id' in request.POST and 'status' in request.POST:
        try:

            suggestedQuestion=get_object_or_404(SuggestedQuestion,id=int(request.POST['que-id']))
            lastLog=suggestedQuestion.post.logs.all().last()
            if (lastLog.type== PostLog.types.Suggest or lastLog.type== PostLog.types.Reject) and request.POST['status']==PostLog.types.Accept:
                post=suggestedQuestion.post
                question=Question.objects.create(post=post,
                                                title=suggestedQuestion.title,
                                                category=suggestedQuestion.category)
                question.tags.add(*suggestedQuestion.tags.all())
                question.save()
                suggestedQuestion.question=question
                suggestedQuestion.save()
                log=PostLog.objects.create(post=post,
                                            moderator=request.user,
                                            author=post.author,
                                            type=PostLog.types.Accept,
                                            )
                
                return HttpResponse('done')
            elif (lastLog.type== PostLog.types.Suggest) and request.POST['status']==PostLog.types.Reject:
                post=suggestedQuestion.post
                log=PostLog.objects.create(post=post,
                            moderator=request.user,
                            author=post.author,
                            type=PostLog.types.Reject,
                            )
                return HttpResponse('done')

        except ValueError:
            return HttpResponse('error')
            # return redirect(reverse('moderators:suggested-questions-await',kwargs={'page':1}))            

    return redirect(reverse('moderators:suggested-questions-await',kwargs={'page':1}))

@forActiveUser
@forModerator
def suggestedAnswersAwait(request,page,mode):
    categoires=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    category=searchVal=order=None
    tagsF=[]
    answers=Answer.objects.all()
    if  mode==PostLog.types.Suggest:
        answers=answers.exclude(
                post__logs__type=PostLog.types.Accept
            ).exclude(
                post__logs__type=PostLog.types.Reject
            )
            
    
    elif mode==PostLog.types.Accept:
           answers=answers.filter(
            post__logs__type=PostLog.types.Accept
        )
    elif mode==PostLog.types.Reject:
          answers=answers.filter(
            post__logs__type=PostLog.types.Reject
        ).exclude(
            post__logs__type=PostLog.types.Accept

        )
    if 'category' in request.GET and request.GET['category']:
        try:
            category=Category.objects.get(pk=request.GET['category'])
            answers=answers.filter(Q(question__category=category)|Q(question__category__parent=category)|Q(question__category__parent__parent=category)|Q(question__category__parent__parent__parent=category))
        except Category.DoesNotExist:
            pass
    if 'search' in request.GET and request.GET['search']:
        answers=answers.filter(Q(tquestion__itle__contains=request.GET['search'])  | Q(question__post__text__contains=request.GET['search']))
        searchVal=request.GET['search']
    if 'tags' in request.GET:
        try:
            tagsIDs=json.loads(request.GET['tags'])
            for tagID in tagsIDs:
                try:    
                    tag=Tag.objects.get(pk=tagID)
                    answers = answers.filter(question__tags=tag)
                    tagsF.append(tag)
                except Tag.DoesNotExist:
                    pass
        except JSONDecodeError:
            pass
    questions=[]
  

    for ans in answers:
        questions.append(ans.question)
    questions=set(questions)
    if 'order' in request.GET:
        order=request.GET['order']
    if  mode==PostLog.types.Suggest:
        questions=Question.orderByLastSuggesAnstDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    if  mode==PostLog.types.Accept:
        questions=Question.orderByLastAccepAnstDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    if  mode==PostLog.types.Reject:
        questions=Question.orderByLastRejectAnsDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)

   
    page=1 if page==0 else page
    count=len(questions)+0
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(questions): return redirect(reverse('moderators:suggested-questions-await',kwargs={'page':1}))
    questions=list(questions)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={
        'categories':categoires,
        'tags':tags,
        'questions':questions,
        'category':category,
        'searchVal':searchVal,
        'tagsF':tagsF,
        'order':order,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'mode':mode
    }
    return render(request,'moderators/answers/answers.html',contxt)


@forActiveUser
@forModerator
def changeSuggestAnswers(request):
    if 'que-id' in request.POST and 'status' in request.POST and 'mode' in request.POST:
        try:
            mode=request.POST['mode']
            status=request.POST['status']
            question=get_object_or_404(Question,id=int(request.POST['que-id']))
            if mode=='S' and (status==PostLog.types.Accept or status==PostLog.types.Reject):
                if status==PostLog.types.Accept:
                    question.post.save()
                answers=question.getSuggestedAnswers()
                for ans in answers:
                    PostLog.objects.create(
                        post=ans.post,
                        type=PostLog.types.Accept if status==PostLog.types.Accept else PostLog.types.Reject,
                        author=ans.post.author,
                        moderator=request.user              
                    )
                return HttpResponse('done')
            elif mode=='R' and status==PostLog.types.Accept :
                question.post.save()
                answers=question.getRejectedAnswers()
                for ans in answers:
                    PostLog.objects.create(
                        post=ans.post,
                        type=PostLog.types.Accept,
                        author=ans.post.author,
                        moderator=request.user              
                    )
                return HttpResponse('done')

        except ValueError:
            return HttpResponse('error')
            # return redirect(reverse('moderators:suggested-questions-await',kwargs={'page':1}))            

    return redirect(reverse('moderators:suggested-answers-await',kwargs={'page':1}))
@forActiveUser
@forModerator
def changeSuggestAnswer(request):
    if 'ans-id' in request.POST and 'status' in request.POST:
        try:
            status=request.POST['status']
            answer=get_object_or_404(Answer,id=int(request.POST['ans-id']))
            lastLogType=answer.post.logs.last().type
            if status==PostLog.types.Accept and ( lastLogType==PostLog.types.Suggest or lastLogType==PostLog.types.Reject):
                answer.question.post.save()
                PostLog.objects.create(
                    post=answer.post,
                    moderator=request.user,
                    author=answer.post.author,
                    type=PostLog.types.Accept
                )
                return HttpResponse('done')

            elif status== PostLog.types.Reject and lastLogType==PostLog.types.Suggest:
                    PostLog.objects.create(
                    post=answer.post,
                    moderator=request.user,
                    author=answer.post.author,
                    type=PostLog.types.Reject
                    )
                    return HttpResponse('done')
        except ValueError:
            pass
    return redirect(reverse('moderators:suggested-answers-await',kwargs={'page':1}))
    