from json.decoder import JSONDecodeError
from django.core.checks.messages import CRITICAL
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from dashboard.decorators import forSuperAdmin
from content.models import Comment, PostLog, Question,Post,Category,Tag,Answer
from math import ceil
from django.contrib import messages
from django.db.models import Count
from interviewsquestions.utilities.datetime import getTimezoneName
import json
@forSuperAdmin
def questions(request,page):
    questions=Question.objects.all()
    if 'search' in request.GET and request.GET['search']:
        if not request.GET['search'].isnumeric():
            questions= questions.filter(title__contains=request.GET['search'])
        else:
            questions=[]
            try:
                questions.append(Question.objects.get(pk=int(request.GET['search'])))
            except Question.DoesNotExist:
                pass
    if 'order' in request.GET:
        if request.GET['order']=='date':
            questions=Question.orderByAcceptDate(questions,False)
        elif request.GET['order']=='date':
            questions=questions.annotate(Count('answers'))
            questions=questions.order_by('count__answers')
    questions=list(questions)
    page=1 if page==0 else page
    count=len(questions)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(questions): return redirect(reverse('dashboard:questions',kwargs={'page':1}))
    questions=list(questions)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={ 
        'questions':questions,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'search' :request.GET['search'] if 'search' in request.GET else None,
        'order' :request.GET['order'] if 'order' in request.GET else None,
    }
    return render(request,'dashboard/questions.html',contxt)

@forSuperAdmin
def deleteQuestion(request):
    if 'del-id' in request.POST and 'page' in request.POST:
        try:
            try:
                post=Post.objects.get(question__id=int(request.POST['del-id']))
                post.delete()
                messages.success(request,'question was delete')
            except Post.DoesNotExist:
                messages.error(request,'question does not exists')
            
            
            return redirect(reverse('dashboard:questions',kwargs={'page':int(request.POST['page'])}))
            
        except ValueError:
            pass
    return redirect(reverse('dashboard:questions',kwargs={'page':1}))

    

@forSuperAdmin
def editQuestion(request,questionID):
    question=get_object_or_404(Question,id=questionID)
    if request.method=='POST':
        if 'que-title' in request.POST and 'que-body' in request.POST and 'category-id' in request.POST and 'tags' in request.POST:
            try:
                tagsIds =json.loads(request.POST['tags'])
                if request.POST['que-title'] and request.POST['que-body'] and tagsIds:
                    question.title=request.POST['que-title']
                    question.category=Category.objects.get(pk=int(request.POST['category-id']))
                    question.tags.clear()
                    for tagId in tagsIds:
                        question.tags.add(Tag.objects.get(pk=int(tagId)))
                    question.post.text=request.POST['que-body']
                    question.post.save()
                    question.save()
                elif not request.POST['que-title']:
                    messages.error(request,'title is empty')
                elif not request.POST['que-body']:
                    messages.error(request,'text is empty')
                elif not tagsIds:
                    messages.error(request,'You should add 1 tag or more')
            except (Category.DoesNotExist,Tag.DoesNotExist,JSONDecodeError):
                pass

    categories=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    contxt={
        'categories':categories,
        'question':question,
        'tags':tags
    }
    return render(request,'dashboard/editQuestion.html',contxt)


@forSuperAdmin
def answers(request,page,questionID=-1):
    answers=Answer.objects.all()
    if not questionID==-1:
        answers=get_object_or_404(Question,id=questionID).getAcceptedAnswers()
    if 'search' in request.GET and request.GET['search'].isnumeric():
        answers=[]
        answers.append(Answer.objects.get(pk=request.GET['search']))
    answers=list(answers)
    page=1 if page==0 else page
    count=len(answers)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(answers): return redirect(reverse('dashboard:all-answers-page',kwargs={'page':1}))
    answers=list(answers)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    
    contxt={
        'answers':answers,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],
        'isAnswerQuestions':True if questionID==-1 else False,
        'QID':questionID
    }
    return render(request,'dashboard/answers.html',contxt)



@forSuperAdmin
def deleteAnswer(request):
    if 'del-id' in request.POST and 'page' in request.POST:
        try:
            try:
                post=Post.objects.get(answer__id=int(request.POST['del-id']))
                post.delete()
                messages.success(request,'answer was delete')
            except Post.DoesNotExist:
                messages.error(request,'answer does not exists')
            
            
            return redirect(reverse('dashboard:all-answers-page',kwargs={'page':int(request.POST['page'])}))
            
        except ValueError:
            pass
    return redirect(reverse('dashboard:all-answers-page',kwargs={'page':1}))


@forSuperAdmin
def editAnswer(request,answerID):
    answer=get_object_or_404(Answer,id=answerID)
    if request.method=='POST':
        if 'answer-body' in request.POST and request.POST['answer-body']:
            answer.post.text=request.POST['answer-body']
            answer.post.save()

    contxt={
        'answer':answer
    }
    return render(request,'dashboard/editAnswer.html',contxt)


@forSuperAdmin
def postComments(request,page,postID):
    comments=get_object_or_404(Post,id=postID).comments.all()
    comments=list(comments)
    page=1 if page==0 else page
    count=len(comments)
    toN=page*25
    fromN=toN-25 if toN>25 else 0
    indcStart=page-3 if page>=4 else 1
    pagesCuont=ceil(count/25)
    remPages=ceil((count-fromN)/25)
    if page>pagesCuont and remPages and len(comments): return redirect(reverse('dashboard:post-comments',kwargs={'page':1}))
    comments=list(comments)[fromN:toN]
    pages=range(indcStart,indcStart+7 if remPages>=7 else page+remPages )
    contxt={
        'comments':comments,
        'PID':postID,
        'currentPage':page,
        'pages': pages if len(pages)>1 else [],

    }
    
    return render(request,'dashboard/postComment.html',contxt)

@forSuperAdmin
def deleteComment(request):
    if 'del-id' in request.POST and 'page' in request.POST:
        try:
            try:
                comment=Comment.objects.get(pk=int(request.POST['del-id']))
                postID=comment.post.id
                comment.delete()
                messages.success(request,'comment was delete')
                return redirect(reverse('dashboard:post-comments',kwargs={'postID':postID,'page':int(request.POST['page'])}))
            except Comment.DoesNotExist:
                messages.error(request,'comment does not exists')
                return redirect(reverse('dashboard:questions',kwargs={'page':1}))
            
        except ValueError:
            pass
    return redirect(reverse('dashboard:questions',kwargs={'page':1}))


@forSuperAdmin
def editComment(request,commentID):
    comment=get_object_or_404(Comment,id=commentID)
    if request.method=='POST':
        if 'comment-text' in request.POST:
            comment.text=request.POST['comment-text']
            comment.save()
    contxt={
        'comment':comment
    }
    return render(request,'dashboard/editComment.html',contxt)

@forSuperAdmin
def postLogs(request,postID):
    logs=PostLog.objects.filter(post_id=postID)
    contxt={
        'logs':logs
    }
    return render(request,'dashboard/postLogs.html',contxt)

@forSuperAdmin
def reviewLog(request,logID):
    log =get_object_or_404(PostLog,id=logID)
    contxt={
        'log':log
    }
    return render(request,'dashboard/reviewLog.html',contxt)



@forSuperAdmin
def toggelPostPublish(requset):
    if 'post-id' in requset.POST:
        try:
            post=Post.objects.get(pk=int(requset.POST['post-id']))
            post.isPublished= not post.isPublished
            post.save()
            if post.isPublished:
                PostLog.objects.create(
                    post=post,
                    author=post.author,
                    moderator=requset.user,
                    type=PostLog.types.Publish
                )
                return HttpResponse('pub')
            else:
                
                PostLog.objects.create(
                    post=post,
                    author=post.author,
                    moderator=requset.user,
                    type=PostLog.types.Unpublish
                )
                return HttpResponse('unpub')
        except (Post.DoesNotExist,ValueError):
            pass
    return HttpResponse('error')


@forSuperAdmin
def toggExamQuestion(request):
    if 'que-id' in request.POST:
        try:
            question=Question.objects.get(pk=int(request.POST['que-id']))
            if not question.forExams:
                question.forExams=True
                question.save()
                firstAns=question.answers.first()
                firstAns.correctAnswer=True
                firstAns.save()
                print(firstAns)
                return HttpResponse('added')
            else:
                question.forExams=False
                question.save()
                try:
                    correctAns=question.answers.get(correctAnswer=True)
                    correctAns.correctAnswer=None
                    correctAns.save()
                
                except Answer.DoesNotExist:
                    pass
                return HttpResponse('removed')
        except Question.DoesNotExist:
            pass

    return HttpResponse('error')


@forSuperAdmin
def markCorrectAnswer(request):
    if 'ans-id' in request.POST:
        try:
            answer=Answer.objects.get(pk=int(request.POST['ans-id']))
            cor=answer.question.answers.get(correctAnswer=True)
            cor.correctAnswer=None
            cor.save()
            answer.correctAnswer=True
            answer.save()
            return HttpResponse(json.dumps({'id':cor.id}))
        except Answer.DoesNotExist:
            pass
    return HttpResponse('error')