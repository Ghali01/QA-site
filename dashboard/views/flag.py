
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls  import reverse
from dashboard.decorators import forSuperAdmin
from feedback.models import FlagReason, Reports
from django.contrib import messages
from content.models import Answer, Question
from math import ceil
@forSuperAdmin
def flagReasons(request,type):
    reasons=FlagReason.objects.filter(type=type)
    contxt={
        'tp':type,
        'reasons':reasons
    }
    return render(request,'dashboard/flagReasons.html',contxt)


@forSuperAdmin
def addReason(request,type):
    if request.method=='POST':
        if 'name-en' in request.POST and 'name-ar' in request.POST and 'desc-en' in request.POST and 'desc-ar' in request.POST:
            FlagReason.objects.create(
                nameEN=request.POST['name-en'],
                nameAR=request.POST['name-ar'],
                descEN=request.POST['desc-en'],
                descAR=request.POST['desc-ar'],
                type=type
               )
            messages.success(request,'reason added')
            return redirect(reverse('dashboard:flag-reasons' ,kwargs={'type':type}))
               
    return render(request,'dashboard/addEditFlagReason.html')

@forSuperAdmin
def deleteReason(request):
    if 'del-id' in request.POST:
        try:
            r=FlagReason.objects.get(pk=int(request.POST['del-id']))
            r.delete()
            messages.success(request,'reason removed')
            return redirect(reverse('dashboard:flag-reasons' ,kwargs={'type':r.type}))
        except (FlagReason.DoesNotExist,ValueError):
            pass
    return redirect(reverse('dashboard:index'))

@forSuperAdmin
def editReason(request,reasonID):
    reason=get_object_or_404(FlagReason,id=reasonID)
    if request.method=='POST':
        if 'name-en' in request.POST and 'name-ar' in request.POST and 'desc-en' in request.POST and 'desc-ar' in request.POST:
                reason.nameEN=request.POST['name-en']
                reason.nameAR=request.POST['name-ar']
                reason.descEN=request.POST['desc-en']
                reason.descAR=request.POST['desc-ar']
                reason.save()
    contxt={
        'reason':reason
    }
    return render(request,'dashboard/addEditFlagReason.html',contxt)



@forSuperAdmin
def flagedQuestions(request,page):
    questions=Question.objects.filter(post__reports__isnull=False)
    page=1 if page==0 else page
    count=questions.count()+0
    toN=page*25
    fromN=toN-25
    questions=list(questions)[fromN:toN]
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    # if page>pagesCuont and remPages: return redirect(f'/dashboard/advertise-messages/{language}/1')
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    questions=set(questions)
    contxt={
        'questions':questions,
        'pages' :pages if len(pages)>1 else [],
        'currentPage':page
    }
    return render(request,'dashboard/flagedQuestions.html',contxt)
@forSuperAdmin
def flagedAnswers(request,page):
    answers=Answer.objects.filter(post__reports__isnull=False)
    page=1 if page==0 else page
    count=answers.count()+0
    toN=page*25
    fromN=toN-25
    answers=list(answers)[fromN:toN]
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    # if page>pagesCuont and remPages: return redirect(f'/dashboard/advertise-messages/{language}/1')
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    answers=set(answers)
    contxt={
        'answers':answers,
        'pages' :pages if len(pages)>1 else [],
        'currentPage':page
    }
    return render(request,'dashboard/flagedAnswers.html',contxt)


@forSuperAdmin
def flagedUsers(request,page):
    users=User.objects.filter(reports__isnull=False)
    page=1 if page==0 else page
    count=users.count()+0
    toN=page*25
    fromN=toN-25
    users=list(users)[fromN:toN]
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    # if page>pagesCuont and remPages: return redirect(f'/dashboard/advertise-messages/{language}/1')
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    users=set(users)
    contxt={
        'users':users,
        'pages' :pages if len(pages)>1 else [],
        'currentPage':page
    }
    return render(request,'dashboard/flagedUsers.html',contxt)



@forSuperAdmin
def removeReports(request):
    if 'type' in request.POST and  'report-on' in request.POST and  'reason-id' in request.POST and request.POST['report-on'].isnumeric() and request.POST['reason-id'].isnumeric():
        if request.POST['type'] == 'Q' or request.POST['type'] == 'A' :
            Reports.objects.filter(post_id=int(request.POST['report-on']),reason_id=int(request.POST['reason-id'])).delete()
            return HttpResponse('done')
        if request.POST['type'] == 'U':
            Reports.objects.filter(user_id=int(request.POST['report-on']),reason_id=int(request.POST['reason-id'])).delete()
        return HttpResponse('done')

    return HttpResponse('error')