
from json.decoder import JSONDecodeError

from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,forModerator
from content.models import  Category, Post, PostLog, Question, SuggestedEdit,Tag,Badge
import json
from math import ceil
from django.shortcuts import get_object_or_404

@forActiveUser
@forModerator
def suggestedEditsAwait(request,page,mode):
    categoires=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    category=searchVal=order=None
    tagsF=[]
    edits=SuggestedEdit.objects.all()
    if  mode==PostLog.types.Suggest:
        edits=edits.filter(status=SuggestedEdit.staties.Suggest)
            
    
    elif mode==PostLog.types.Accept:
        edits=edits.filter(status=SuggestedEdit.staties.Accept).distinct('post__question','post__answer__question')
    elif mode==PostLog.types.Reject:
        edits=edits.filter(status=SuggestedEdit.staties.Reject)
     
    if 'category' in request.GET and request.GET['category']:
        try:
            category=Category.objects.get(pk=request.GET['category'])
            edits=edits.filter(
            Q(
                Q(post__type=Post.types.Question)&
                Q(
                    Q(post__question__category=category)|
                    Q(post__question__category__parent=category)|
                    Q(post__question__category__parent__parent=category)|
                    Q(post__question__category__parent__parent__parent=category)
                )
            )|Q(
                Q(post__type=Post.types.Answer)&
                Q(
                    Q(post__answer__question__category=category)|
                    Q(post__answer__question__category__parent=category)|
                    Q(post__answer__question__category__parent__parent=category)|
                    Q(post__answer__question__category__parent__parent__parent=category)
                )
            )
        )
        except Category.DoesNotExist:
            pass
    if 'search' in request.GET and request.GET['search']:
        edits=edits.filter(Q(Q(post__type=Post.types.Question)&Q(post__question__title__contains=request.GET['search'])  |
         Q(post__question__post__text__contains=request.GET['search']))|
         Q(Q(post__type=Post.types.Answer)&Q(post__answer__question__title__contains=request.GET['search'])  |
         Q(post__answer__question__post__text__contains=request.GET['search']))
         )
        searchVal=request.GET['search']
    if 'tags' in request.GET:
        try:
            tagsIDs=json.loads(request.GET['tags'])
            for tagID in tagsIDs:
                try:    
                    tag=Tag.objects.get(pk=tagID)
                    edits = edits.filter(
                        Q(Q(post__type=Post.types.Question)&Q(post__question__tags=tag))|
                        Q(Q(post__type=Post.types.Answer)&Q(post__answer__question__tags=tag))
                        )
                    tagsF.append(tag)
                except Tag.DoesNotExist:
                    pass
        except JSONDecodeError:
            pass
 
    if 'order' in request.GET:
        order=request.GET['order']
    if  mode==PostLog.types.Suggest:
        edits=SuggestedEdit.orderBySuggestDate(edits,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    if  mode==PostLog.types.Accept:
        edits=SuggestedEdit.orderByAcceptDate(edits,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)
    if  mode==PostLog.types.Reject:
        edits=SuggestedEdit.orderByRejectDate(edits,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)

    # print(edits)
    # for e in edits:
    #     print(e.post.id)
    page=1 if page==0 else page
    count=len(edits)+0
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(edits): return redirect(reverse('moderators:suggested-edits-await',kwargs={'page':1}))
    edits=list(edits)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={
        'categories':categoires,
        'tags':tags,
        'edits':edits,
        'category':category,
        'searchVal':searchVal,
        'tagsF':tagsF,
        'order':order,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'mode':mode
    }
    return render(request,'moderators/edits/edits.html',contxt)
@forActiveUser
@forModerator
def suggestedEditsAccepted(request,page,mode):
    categoires=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    category=searchVal=order=None
    tagsF=[]
    questions=Question.objects.filter(post__logs__type=PostLog.types.AcceptEdit)
    if 'category' in request.GET and request.GET['category']:
        try:
            category=Category.objects.get(pk=request.GET['category'])
            questions=questions.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category)|Q(category=category))
            
        except Category.DoesNotExist:
            pass
    if 'search' in request.GET and request.GET['search']:
        searchVal=request.GET['search']
        questions=questions.filter(Q(post__text=searchVal)|Q(title=searchVal))
    if 'tags' in request.GET:
        try:
            tagsIDs=json.loads(request.GET['tags'])
            for tagID in tagsIDs:
                try:    
                    tag=Tag.objects.get(pk=tagID)
                    questions=questions(tags=tag)
                    tagsF.append(tag)
                except Tag.DoesNotExist:
                    pass
        except JSONDecodeError:
            pass
 
    if 'order' in request.GET:
        order=request.GET['order']
        questions=Question.orderByLastAccepAnstDate(questions,asc=True if 'order' in request.GET and request.GET['order']=='O' else False)

    page=1 if page==0 else page
    count=len(questions)+0
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(questions): return redirect(reverse('moderators:suggested-edits-await',kwargs={'page':1}))
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
    return render(request,'moderators/edits/edits.html',contxt)

@forActiveUser
@forModerator
def reviewEdit(request,editID):
    edit=get_object_or_404(SuggestedEdit,id=editID)
    contxt={
        'edit':edit
    }
    return render(request,'moderators/edits/reviewEdit.html',contxt)

@forActiveUser
@forModerator
def changeSuggestedEditStatus(request):
    if 'edit-id'  in request.POST and 'status' in request.POST:
        try:
            edit=get_object_or_404(SuggestedEdit,id=int(request.POST['edit-id']))
            if request.POST['status']==SuggestedEdit.staties.Accept and(edit.status== SuggestedEdit.staties.Suggest or edit.status== SuggestedEdit.staties.Reject):
                edit.status=SuggestedEdit.staties.Accept
                edit.save()
                edit.post.text=edit.text()
                edit.post.save()
                log=PostLog.objects.create(
                    post=edit.post,
                    author=edit.userWhoSugget(),
                    moderator=request.user,
                    type=PostLog.types.AcceptEdit,
                    edit=edit,
                    originLog=edit.logs.get(type=PostLog.types.SuggestEdit)

                )
                countEditsBadge(edit)
                return HttpResponse('done')
            elif request.POST['status']==SuggestedEdit.staties.Reject and edit.status==SuggestedEdit.staties.Suggest:
                edit.status=SuggestedEdit.staties.Reject
                edit.save()
                log=PostLog.objects.create(
                    post=edit.post,
                    author=edit.userWhoSugget(),
                    moderator=request.user,
                    type=PostLog.types.RejectEdit,
                    edit=edit,
                    originLog=edit.logs.get(type=PostLog.types.SuggestEdit)

                )
                return HttpResponse('done')
        except ValueError:
            pass
    return HttpResponse('error')





def countEditsBadge(edit):
    user=edit.userWhoSugget()
    userBadges=user.profile.badges.all()
    badgesG=Badge.objects.filter(reason=Badge.reasons.Edits,targetType=Badge.targetTypes.General).difference(userBadges)
    editsCountG=PostLog.objects.filter(author=user,type=PostLog.types.AcceptEdit).count()
    for badge in badgesG:
        if badge.count <= editsCountG:
            user.profile.badges.add(badge)
    question=edit.post.getQuestion()
    badgesC=Badge.objects.filter(reason=Badge.reasons.Edits,category_id=question.category.id).difference(userBadges)
    editsCountC=PostLog.objects.filter(Q(author=user)&Q(type=PostLog.types.AcceptEdit)&Q(Q(post__question__category=question.category)|Q(post__answer__question__category=question.category))).count()
    for badge in badgesC:
        if badge.count <= editsCountC:
            user.profile.badges.add(badge)

    for tag in question.tags.all():
        badgesT= Badge.objects.filter(reason=Badge.reasons.Edits,tag=tag).difference(userBadges)
        for badge in badgesT:
            if badge.count <= PostLog.objects.filter(Q(author=user)&Q(type=PostLog.types.AcceptEdit)&Q(Q(post__question__tags=tag)|Q(post__answer__question__tags=tag))).count():
                user.profile.badges.add(badge)
