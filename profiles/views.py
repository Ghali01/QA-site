from django.shortcuts import render
from django.http import HttpResponse
from content.models import Answer, Question
from django.db.models import Count,F
from math import ceil
from django.template.loader import render_to_string
import json
def profilePage(request,userID):
    return HttpResponse(userID)

def userQuestions(request,userID):
    votesFilter=answersFilter=viewsFilter=searchVal=None
    questions=Question.objects.filter(post__author__id=userID)
    if 'search' in request.GET and request.GET['search']:
        searchVal=request.GET['search']
        questions=questions.filter(title__contains=request.GET['search'])
    
    questions=questions.annotate(Count(F('answers')))
    
    orderFields=[
        '-post__ActiveDate',
        
        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
        'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count' ,
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
        '-post__ActiveDate',

        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
        'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count' ,

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
    answers=Answer.objects.filter(post__author__id=userID)
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
    answers=Answer.objects.filter(post__author__id=userID)
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
        