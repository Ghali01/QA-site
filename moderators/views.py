
from json.decoder import JSONDecodeError

from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,forModerator
from content.models import Category, Post, PostLog, Question,Tag,SuggestedQuestion
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
            questions=SuggestedQuestion.objects.filter(category=category)
        except Category.DoesNotExist:
            pass
    if 'search' in request.GET and request.GET['search']:
        questions=questions.filter(Q(title__contains=request.GET['search'])  | Q(post__text__contains=request.GET['search']))
        searchVal=request.GET['search']
    if 'order' in request.GET and request.GET['order']=='O':
        questions=questions.order_by('-date')
        order=request.GET['order']
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
  
    if category:
        questions=questions.union(*subCategoriesSuggestedQuestions(category.subCategoies(),request,mode))
    page=1 if page==0 else page
    count=questions.count()+0
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


def subCategoriesQuestions(subCategories,request,mode):
    sets=[]
    for subCategory in subCategories:
        questions=Question.objects.filter(category=subCategory)
        if  mode==PostLog.types.Suggest:
            questions=questions.exclude(
                answers__post__logs__type=PostLog.types.Accept
            ).exclude(
                answers__post__logs__type=PostLog.types.Reject
            )
            
        elif mode==PostLog.types.Accept:
            questions=questions.filter(
                answers__post__logs__type=PostLog.types.Accept
            )
        elif mode==PostLog.types.Reject:
            questions=questions.filter(
                answers__post__logs__type=PostLog.types.Reject
            ).exclude(
                answers__post__logs__type=PostLog.types.Accept
                )
        if 'search' in request.GET and request.GET['search']:
            questions=questions.filter(Q(title__contains=request.GET['search'])  | Q(post__text__contains=request.GET['search']))
        if 'order' in request.GET and request.GET['order']=='O':
            questions=questions.order_by('-date')
        if 'tags' in request.GET:
            try:
                tagsIDs=json.loads(request.GET['tags'])
                for tagID in tagsIDs:
                    try:    
                        questions = questions.filter(tags=Tag.objects.get(pk=tagID))
                    except Tag.DoesNotExist:
                        pass
            except JSONDecodeError:
                pass
        sets.append(questions)
    return sets


def subCategoriesSuggestedQuestions(subCategories,request,mode):
    sets=[]
    for subCategory in subCategories:
        questions=SuggestedQuestion.objects.filter(category=subCategory)
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

        if 'search' in request.GET and request.GET['search']:
            questions=questions.filter(Q(title__contains=request.GET['search'])  | Q(post__text__contains=request.GET['search']))
        if 'order' in request.GET and request.GET['order']=='O':
            questions=questions.order_by('-date')
        if 'tags' in request.GET:
            try:
                tagsIDs=json.loads(request.GET['tags'])
                for tagID in tagsIDs:
                    try:    
                        questions = questions.filter(tags=Tag.objects.get(pk=tagID))
                    except Tag.DoesNotExist:
                        pass
            except JSONDecodeError:
                pass
        sets.append(questions)
    return sets

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
    questions=Question.objects.all()
    if  mode==PostLog.types.Suggest:
            questions=questions.exclude(
                answers=None
        ).exclude(
        answers__post__logs__type=PostLog.types.Accept
        ).exclude(
            answers__post__logs__type=PostLog.types.Reject

        )
    elif mode==PostLog.types.Accept:
           questions=questions.filter(
            answers__post__logs__type=PostLog.types.Accept
        )
    elif mode==PostLog.types.Reject:
          questions=questions.filter(
            answers__post__logs__type=PostLog.types.Reject
        ).exclude(
            answers__post__logs__type=PostLog.types.Accept

        )
    if 'category' in request.GET and request.GET['category']:
        try:
            category=Category.objects.get(pk=request.GET['category'])
            questions=questions.filter(category=category)
        except Category.DoesNotExist:
            pass
    if 'search' in request.GET and request.GET['search']:
        questions=questions.filter(Q(title__contains=request.GET['search'])  | Q(post__text__contains=request.GET['search']))
        searchVal=request.GET['search']
    if 'order' in request.GET and request.GET['order']=='O':
        questions=questions.order_by('-date')
        order=request.GET['order']
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
    print(questions)
  
    if category:
        questions=questions.union(*subCategoriesQuestions(category.subCategoies(),request,mode))
    page=1 if page==0 else page
    count=questions.count()+0
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


