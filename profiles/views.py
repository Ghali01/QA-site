from django.shortcuts import render
from django.http import HttpResponse
from content.models import Question
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
        searchVal=request.GET['search']
        questions=questions.filter(title__contains=request.GET['search'])
    
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
        