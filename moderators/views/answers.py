
from json.decoder import JSONDecodeError
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,forModerator
from content.models import Answer, Category,  PostLog, Question,Tag,Badge
import json
from math import ceil
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
@forActiveUser
@forModerator
def suggestedAnswersAwait(request,page,mode):
    language=get_language()[:2]
    categoires=Category.objects.filter(language=language,parent=None)
    tags=Tag.objects.filter(category__language=language)
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
    category=request.user.profile.category
    
    if 'category' in request.GET and request.GET['category']:
        try:
            category=Category.objects.get(pk=request.GET['category'])
        except Category.DoesNotExist:
            category=request.user.profile.category
    else:
        category=request.user.profile.category

    
    answers=answers.filter(Q(question__category=category)|Q(question__category__parent=category)|Q(question__category__parent__parent=category)|Q(question__category__parent__parent__parent=category))
    if 'search' in request.GET and request.GET['search']:
        answers=answers.filter(Q(question__title__contains=request.GET['search'])  | Q(question__post__text__contains=request.GET['search']))
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
        questions=Question.orderByLastRejectAnstDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)

   
    page=1 if page==0 else page
    count=len(questions)+0
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(questions): return redirect(reverse('moderators:suggested-answers-await',kwargs={'page':1}))
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
        # try:
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
                        moderator=request.user,
                        originLog=ans.post.logs.get(type=PostLog.types.Suggest)
              
                    )
                    countAnswersBadge(ans)
                countSelfAnswersBadge(question)

                return HttpResponse('done')
            elif mode=='R' and status==PostLog.types.Accept :
                question.post.save()
                answers=question.getRejectedAnswers()
                for ans in answers:
                    PostLog.objects.create(
                        post=ans.post,
                        type=PostLog.types.Accept,
                        author=ans.post.author,
                        moderator=request.user,
                        originLog=ans.post.logs.get(type=PostLog.types.Suggest)
                                      
                    )
                return HttpResponse('done')

        # except ValueError:
        #     return HttpResponse('error')
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
                    type=PostLog.types.Accept,
                    originLog=answer.post.logs.get(type=PostLog.types.Suggest)

                )

                countAnswersBadge(answer)
                countSelfAnswersBadge(answer.question)
                return HttpResponse('done')

            elif status== PostLog.types.Reject and lastLogType==PostLog.types.Suggest:
                    PostLog.objects.create(
                    post=answer.post,
                    moderator=request.user,
                    author=answer.post.author,
                    type=PostLog.types.Reject,
                    originLog=answer.post.logs.get(type=PostLog.types.Suggest)

                    )
                    return HttpResponse('done')
        except ValueError:
            pass
    return redirect(reverse('moderators:suggested-answers-await',kwargs={'page':1}))

def countAnswersBadge(answer):
    userBadges=answer.post.author.profile.badges.all()
    badgesG=Badge.objects.filter(reason=Badge.reasons.Answers,targetType=Badge.targetTypes.General).difference(userBadges)
    answersCountG= Answer.objects.filter(post__author=answer.post.author,post__logs__type=PostLog.types.Accept).count()
    for badge in badgesG:
        if badge.count <=answersCountG:
            answer.post.author.profile.badges.add(badge)
    badgesC=Badge.objects.filter(reason=Badge.reasons.Answers,category_id=answer.question.category.id).difference(userBadges)
    answersCountC=Answer.objects.filter(post__author=answer.post.author,post__logs__type=PostLog.types.Accept,question__category=answer.question.category).count()
    for badge in badgesC:
        if badge.count <= answersCountC:
            answer.post.author.profile.badges.add(badge)

    for tag in answer.question.tags.all():
        badgesT= Badge.objects.filter(reason=Badge.reasons.Answers,tag=tag).difference(userBadges)
        for badge in badgesT:
            if badge.count <= Answer.objects.filter(post__author=answer.post.author,post__logs__type=PostLog.types.Accept,question__tags=tag).count():
                answer.post.author.profile.badges.add(badge)

def countSelfAnswersBadge(question):
    badges=Badge.objects.filter(
        Q(reason=Badge.reasons.SelfAnswers)&
        Q(
            Q(category_id=question.category.id)|
            Q(targetType=Badge.targetTypes.General)
        
        ))
    for tag in question.tags.all():
        badges= badges.union(Badge.objects.filter(reason=Badge.reasons.SelfAnswers,tag=tag))
    badges=badges.difference(question.post.author.profile.badges.all())
    for badge in badges:
        if badge.count <= question.getAcceptedAnswers().count():
            question.post.author.profile.badges.add(badge)
