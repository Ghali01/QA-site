from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from content.models import Answer, Badge, Post, PostLog, Question,Category
from django.db.models import Count,F
from math import ceil
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import json
def profilePage(request,userID):
    ptype=order=None
    user=get_object_or_404(User,id=userID)
    user.profile.views=F('views')+1
    user.profile.save()
    user.profile.refresh_from_db()
    topPosts=Post.objects.filter(author=user,logs__type=PostLog.types.Accept)
    if 'ptype' in request.GET:
        ptype=request.GET['ptype']
        if request.GET['ptype']=='Q':
            topPosts=topPosts.filter(type=Post.types.Question)
        elif request.GET['ptype']=='A':
            topPosts=topPosts.filter(type=Post.types.Answer)
    if 'order' in request.GET:
        order=request.GET['order']
        if request.GET['order']=="V":
            topPosts= topPosts.order_by('-votes')
        if request.GET['order']=='N':
            topPosts=topPosts.order_by('-id')
    topPosts=topPosts[:7]
    for post in topPosts:
        post.suggestTime=post.logs.get(type=PostLog.types.Suggest).time
    contxt={
        'user':user,
        'topPosts':topPosts,
        'tab':'profile',
        'order':order,
        'ptype':ptype
    }
    return render(request,'profiles/profile.html',contxt)

def userQuestions(request,userID):
    votesFilter=answersFilter=viewsFilter=searchVal=None
    questions=Question.objects.filter(post__author__id=userID)
    if 'search' in request.GET and request.GET['search']:
        searchVal=request.GET['search']
        questions=questions.filter(title__contains=request.GET['search'])
    
    questions=questions.annotate(Count(F('answers')))
    
    orderFields=[
        
        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
        'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count' ,
        '-post__ActiveDate',
    ]
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
        'questions':questions,
        'pageCount':pageCount,
        'votesFilter':votesFilter,
        'viewsFilter':viewsFilter,
        'answersFilter':answersFilter,
        'searchVal':searchVal if searchVal else '',
        'userID':userID
    }
    return render(request,'profiles/userQuestions.html',contxt)


def seeMoreQuestions(request,userID,page):
    questions=Question.objects.filter(post__author__id=userID)
    if 'search' in request.GET and request.GET['search']:
        questions=questions.filter(title__contains=request.GET['search'])
    
    questions=questions.annotate(Count(F('answers')))
    
    orderFields=[

        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
        'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count' ,

        '-post__ActiveDate',
    ]
    questions=questions.order_by(*orderFields)
  
    remPages=int(ceil(questions.count()/15)-page-1)
    questions=questions[page*15:(page*15)+15]

    htmlStr=''
    for que in questions:
        htmlStr+= render_to_string('content/templatetags/questionitem.html',{'question':que})
    return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))
        
def userAnswers(request,userID):
    votesFilter=viewsFilter=searchVal=None
    answers=Answer.objects.filter(post__author__id=userID,post__isPublished=True,question__post__isPublished=True)
    if 'search' in request.GET and request.GET['search']:
        searchVal=request.GET['search']
        answers=answers.filter(question__title__contains=request.GET['search'])
    
    
    orderFields=[
        
        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'question__views' if 'views' in request.GET and request.GET['views']=='L' else '-question__views',

    ]
    
    answers=answers.order_by(*orderFields)
    if 'votes' in request.GET:
        votesFilter=request.GET['votes']
    if 'views' in request.GET:
        viewsFilter=request.GET['views']
    questions=[]
    for ans in answers:
        if not ans.question in questions:
            questions.append(ans.question)    
    
    pageCount=ceil(len(questions)/15)
    questions=questions[:15]
    contxt={
        'questions':questions,
        'pageCount':pageCount,
        'votesFilter':votesFilter,
        'viewsFilter':viewsFilter,
        'searchVal':searchVal if searchVal else '',
        'userID':userID
    }
    return render(request,'profiles/userAnswers.html',contxt)


def seeMoreAnswers(request,userID,page):
    answers=Answer.objects.filter(post__author__id=userID,post__isPublished=True,question__post__isPublished=True)
    if 'search' in request.GET and request.GET['search']:
        answers=answers.filter(question__title__contains=request.GET['search'])
    
    
    orderFields=[
        
        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'question__views' if 'views' in request.GET and request.GET['views']=='L' else '-question__views',

    ]
    answers=answers.order_by(*orderFields)
    questions=[]
    for ans in answers:
        if not ans.question in questions:
            questions.append(ans.question)    
        
    remPages=int(ceil(len(questions)/15)-page-1)
    questions=questions[page*15:(page*15)+15]

    htmlStr=''
    for que in questions:
        htmlStr+= render_to_string('content/templatetags/questionitem.html',{'question':que})
    return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))
        

def userBadges(request,userID):
    user=get_object_or_404(User,id=userID)
    goldBadges=user.profile.goldBadges()
    for badge in goldBadges:
        badge.isEraned=True
    goldBadges=list(goldBadges)+list(Badge.objects.filter(level=Badge.levels.Gold))
    goldBadges=goldBadges[:5]
    silverBadges=user.profile.silverBadges()
    for badge in silverBadges:
        badge.isEraned=True
    silverBadges=list(silverBadges)+list(Badge.objects.filter(level=Badge.levels.Silver))
    silverBadges=silverBadges[:5]
    bronzeBadges=user.profile.bronzeBadges()
    for badge in bronzeBadges:
        badge.isEraned=True
    bronzeBadges=list(bronzeBadges)+list(Badge.objects.filter(level=Badge.levels.Bronze))
    bronzeBadges=bronzeBadges[:5]
    contxt={
        'user':user,
        'goldBadges':goldBadges,
        'silverBadges':silverBadges,
        'bronzeBadges':bronzeBadges,
        'tab':'badges'

    }
    return render(request,'profiles/badges.html',contxt)

def seeMoreBadges(request,page):
    if 'user-id' in request.GET and 'level' in request.GET:
        try:
            user=get_object_or_404(User,id=int(request.GET['user-id']))
            badges=[] 
            if request.GET['level']==Badge.levels.Gold: 
                badges=user.profile.goldBadges()
                for badge in badges:
                    badge.isEraned=True
                badges=list(badges)+list(Badge.objects.filter(level=Badge.levels.Gold))
            if request.GET['level']==Badge.levels.Silver: 
                badges=user.profile.silverBadges()
                for badge in badges:
                    badge.isEraned=True
                badges=list(badges)+list(Badge.objects.filter(level=Badge.levels.Silver))
            if request.GET['level']==Badge.levels.Bronze: 
                badges=user.profile.bronzeBadges()
                for badge in badges:
                    badge.isEraned=True
                badges=list(badges)+list(Badge.objects.filter(level=Badge.levels.Bronze))
            remPages=int(ceil(len(badges)/10)-page-1)
            badges=badges[page*10:(page*10)+10]
            htmlStr=''
            for badge in badges:
                htmlStr+=render_to_string('profiles/templatetags/badgeItem.html',{'badge':badge})
            return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))
        except ValueError:
            pass
        return HttpResponse('error')

def userFollowers(request,userID):
    user=get_object_or_404(User,id=userID)
    
    followers=user.profile.followers.all()
    pageCount=ceil(followers.count()/15)
    
    followers=followers[:15]
    contxt={
        'user':user,
        'tab':'followers',    
        'followers':followers,
        'pageCount':pageCount
    }

    return render(request,'profiles/followers.html',contxt)

def seeMoreFollowers(request,page):
    if 'user-id' in request.GET:
        try:
            user=get_object_or_404(User,id=request.GET['user-id'])
            followers=user.profile.followers.all()
            remPages=int(ceil(len(followers)/15)-page-1)
            followers=followers[page*15:(page*15)+15]
            htmlStr=''
            for person in followers:
                htmlStr+=render_to_string('profiles/templatetags/followerItem.html',{'person':person,'user':request.user})
            return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))
        except ValueError:
            pass
    return HttpResponse('error')


def favQuestion(request,userID):
    viewsFilter=votesFilter=answersFilter=category=categoryID=None
    user=get_object_or_404(User,id=userID)
    categories=Category.objects.filter(parent=None)
    if 'category' in request.GET:
        try:
            category=get_object_or_404(Category,id=int(request.GET['category']))
            categoryID=int(request.GET['category'])
        except (Category.DoesNotExist,ValueError):
            pass
    questions=user.profile.favQuestions.all()
    if category:
        questions=questions.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category))
    questions=questions.annotate(Count(F('answers')))
    orderFields=[
        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
        'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count' ,
        '-post__ActiveDate',

    ]
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
        'user':user,
        'tab':'favorite',
        'category':category,
        'categories':categories,
        'questions':questions,
        'votesFilter':votesFilter,
        'viewsFilter':viewsFilter,
        'answersFilter':answersFilter,
        'categoryID':categoryID ,
        'pageCount':pageCount,

    }
    return render(request,'profiles/favoriteQuestions.html',contxt)

def seeMoreFavQuestion(request,page):
    if 'user-id' in request.GET:
        try:
            user=get_object_or_404(User,id=int(request.GET['user-id']))
            questions=user.profile.favQuestions.all()

            if 'category' in request.GET and request.GET['category'].isnumeric:
                category=int(request.GET['category'])
                questions=questions.filter(Q(category_id=category)|Q(category__parent_id=category)|Q(category__parent__parent_id=category)|Q(category__parent__parent__parent_id=category))
            questions=questions.annotate(Count(F('answers')))
            orderFields=[
                'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
                'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
                'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count' ,
                '-post__ActiveDate',

            ]
            questions=questions.order_by(*orderFields)
            remPages=int(ceil(questions.count()/15)-page-1)
            questions=questions[page*15:(page*15)+15]

            htmlStr=''
            for que in questions:
                htmlStr+= render_to_string('content/templatetags/questionitem.html',{'question':que})
            return HttpResponse(json.dumps({'html':htmlStr,'remPages':remPages}))

        except (ValueError):
            pass
    return HttpResponse('error')