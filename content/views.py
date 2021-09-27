import datetime
from json.decoder import JSONDecodeError
from math import ceil
from django.contrib.auth.models import PermissionsMixin, User
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser, forModerator,userHasTags
from content.models import Badge, Category, PostLog, SuggestedEdit,Tag,SuggestedQuestion,Post,Question, Voter,Answer,Comment
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models.expressions import F,Q
from django.db.models import Count
from django.template.loader import render_to_string
import json
from django.http import Http404 
def index(request,categoryID=-1):
    tagsFilter=viewsFilter=votesFilter=answersFilter=timeFilter=None
    category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
    questions=Question.objects.filter(post__isPublished=True)
    if category:
        questions=questions.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category))
    if 'time' in request.GET:
        timeFilter=request.GET['time']
        if request.GET['time']=='T':
            logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date=datetime.datetime.now().date())
            questions=questions.filter(post__logs__in=logs)
        elif request.GET['time']=='W':
            logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date__range=(datetime.datetime.now().date()-datetime.timedelta(days=7),datetime.datetime.now().date()))
            questions=questions.filter(post__logs__in=logs)
        elif request.GET['time']=='M':               
            logs=PostLog.objects.filter(type=PostLog.types.Accept,post__type=Post.types.Question,time__date__range=(datetime.datetime.now().date()-datetime.timedelta(days=30),datetime.datetime.now().date()))
            questions=questions.filter(post__logs__in=logs)
        
    if 'tags' in request.GET and request.GET['tags']=='M' and request.user.is_authenticated and not request.user.is_anonymous:
        tagsFilter=request.GET['tags']
        for tag in request.user.profile.tags.all():
            questions=questions.filter(tags=tag)

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
        'category':category,
        'questions':questions,
        'votesFilter':votesFilter,
        'viewsFilter':viewsFilter,
        'answersFilter':answersFilter,
        'tagsFilter':tagsFilter,
        'categoryID':categoryID if not categoryID==-1 else None,
        'pageCount':pageCount,
        'timeFilter':timeFilter
    }
    return render(request,'content/index.html',contxt)

def seeMoreQueIndex(request,page,categoryID=-1):
    category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
    questions=Question.objects.filter(post__isPublished=True)
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
        for tag in request.user.profile.tags.all():
            questions=questions.filter(tags=tag)
    questions=questions.annotate(Count(F('answers')))
    
    orderFields=[

        '-post__ActiveDate',
   
        'post__votes' if 'votes' in request.GET and request.GET['votes']=='L' else '-post__votes',
        'views' if 'views' in request.GET and request.GET['views']=='L' else '-views',
        'answers__count' if 'answers' in request.GET and request.GET['answers']=='L' else '-answers__count',

    ]
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
                    PostLog.objects.create(post=post,text=post.text,author=request.user,type=PostLog.types.Suggest)
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
    if  not question.post.isPublished and not ( request.user==question.post.author or request.user.profile.isModerator() or request.user.profile.isSuperAdmin() or request.user.profile.isAdmin() ):
        raise Http404
    question.views=F('views')+1
    question.save()
    question.refresh_from_db()
    countViewBadge(question)
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
                countVotesBadges(post)
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
            questions=Question.objects.filter(post__isPublished=True)
            questions=questions.filter(Q(category__id=category)|Q(category__parent__id=category)|Q(category__parent__parent__id=category)|Q(category__parent__parent__parent__id=category))
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
            try:
                post=Post.objects.get(pk=int(requset.POST['post-id']))
                comment=Comment.objects.create( text=requset.POST['text'],
                                                post=post,
                                                author=requset.user    
                                                )
                countCommentBadge(comment)
                countSelfComments(post)
                contxt={
                    'comment':comment
                }
                html=render_to_string('content/templatetags/commentItem.html',contxt)
                return HttpResponse(html)
            except(ValueError,Post.DoesNotExist):
                pass

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
    
@forActiveUser
@userHasTags
def suggestPostEdit(request,postID):
    if request.method=='POST':
        if 'post-body' in request.POST:
            post=get_object_or_404(Post,id=postID)
            edit=SuggestedEdit.objects.create(status=SuggestedEdit.staties.Suggest,post=post)
            log=PostLog.objects.create(post=post,
            text=request.POST['post-body'],
            author=request.user,
            type=PostLog.types.SuggestEdit,
            edit=edit)
            messages.success(request,'The edit has been submitted, it will be reviewed soon.')
            return redirect(reverse('content:question-page',kwargs={'questionID':post.getQuestion().id})+'#mgss')

    post=get_object_or_404(Post,id=postID)
    contxt={
        'post':post
    }
    return render(request,'content/suggestEdit.html',contxt)
def tagsPage(request):
    categories=Category.objects.filter(parent=None)
    tags=Tag.objects.all()
    category=ansFilter=queFilter=None
    if 'category' in request.GET:
        try:
            category=Category.objects.get(pk=int(request.GET['category']))
            tags=tags.filter(Q(category=category)|Q(category__parent=category)|Q(category__parent__parent=category)|Q(category__parent__parent__parent=category))
        except(Category.DoesNotExist,ValueError):
            pass
    
    tags=tags.annotate(answersCount=Count(F('questions__answers')),questionsCount=Count(F('questions')))
    orderFields=[
        'answersCount' if 'answers' in request.GET and request.GET['answers']=='L' else '-answersCount',
        'questionsCount' if 'questions' in request.GET and request.GET['questions']=='L' else '-questionsCount'

    ]
    tags=tags.order_by(*orderFields)
    
    contxt={
        'categories':categories,
        'category':category,
        'queFilter':queFilter,
        'ansFilter':ansFilter,
        'tags':tags
    }
    return render(request,'content/categoryTags.html',contxt)
@forActiveUser
def toggleTagToFav(request):
    if 'tag-id' in request.POST:
        try:
            userTags=request.user.profile.tags
            tag=Tag.objects.get(pk=int(request.POST['tag-id']))
            if tag in userTags.all():
                userTags.remove(tag)
                return HttpResponse('removed')
            else:
                userTags.add(tag)
                return HttpResponse('added')
        except(Tag.DoesNotExist,ValueError):
            pass
    return HttpResponse('error')


def categoriesPage(request):
    tagsFiltr=order=category=None
    categories=Category.objects.filter(parent=None)
    catgoriesList=Category.objects.all()
    if 'category' in request.GET:
        try:
            category=Category.objects.get(pk=request.GET['category'])
            catgoriesList=catgoriesList.filter(Q(parent=category)|Q(parent__parent=category)|Q(parent__parent__parent=category))
        except (Category.DoesNotExist,ValueError):
            pass
    catgoriesList=catgoriesList.annotate(subCategoriesCount=Count(F('categories')))
    orderFields=[

        'subCategoriesCount' if 'tags' in request.GET and request.GET['tags']=='L' else '-subCategoriesCount',
        'time' if 'order' in request.GET and request.GET['order']=='O' else '-time',

    ]
    catgoriesList=catgoriesList.order_by(*orderFields)
    if 'order' in request.GET:
        order=request.GET['order']
    if 'tags' in request.GET:
        tagsFiltr=request.GET['tags']

    contxt={
        'categories':categories,
        'category':category,
        'catgoriesList':catgoriesList,
        'order':order,
        'tagsFiltr':tagsFiltr
    }
    return render(request,'content/categories.html',contxt)


@forActiveUser
@userHasTags
def toggQuestionFav(request):
    if 'que-id' in request.POST:
        try:
            question=Question.objects.get(pk=int(request.POST['que-id']))
            favUserQuestions=request.user.profile.favQuestions
            if not question in favUserQuestions.all():
                favUserQuestions.add(question)
                return HttpResponse('added')
            else:
                favUserQuestions.remove(question)
                return HttpResponse('removed')
        except (Question.DoesNotExist,ValueError):
            pass

    return HttpResponse('error')


def toggUserFollow(request):
    if 'user-id' in request.POST:
        try:
            user=User.objects.get(pk=int(request.POST['user-id']))
            userFollowers=user.profile.followers
            if not request.user in userFollowers.all():
                userFollowers.add(request.user)
                return HttpResponse('added')
            else:
                userFollowers.remove(request.user)
                return HttpResponse('removed')
        except (User.DoesNotExist,ValueError):
            pass
    return HttpResponse('error')

def countCommentBadge(comment):
    userBadges=comment.author.profile.badges.all()
    badgesG=Badge.objects.filter(reason=Badge.reasons.Comments,targetType=Badge.targetTypes.General).difference(userBadges)
    commentsCountG=Comment.objects.filter(author=comment.author).count()
    for badge in badgesG:
        if badge.count <= commentsCountG:
            comment.author.profile.badges.add(badge)
    question=comment.post.getQuestion()
    badgesC=Badge.objects.filter(reason=Badge.reasons.Comments,category_id=question.category.id).difference(userBadges)
    commentsCountC=Comment.objects.filter(Q(author=comment.author)&Q(Q(post__question__category=question.category)|Q(post__answer__question__category=question.category))).count()
    for badge in badgesC:
        if badge.count <= commentsCountC:
            comment.author.profile.badges.add(badge)

    for tag in question.tags.all():
        badgesT= Badge.objects.filter(reason=Badge.reasons.Comments,tag=tag).difference(userBadges)
        for badge in badgesT:
            if badge.count <= Comment.objects.filter(Q(author=comment.author)&Q(Q(post__question__tags=tag)|Q(post__answer__question__tags=tag))).count():
                comment.author.profile.badges.add(badge)


def countSelfComments(post):
    question=post.getQuestion()
    badges=Badge.objects.filter(
        Q(reason=Badge.reasons.SelfComments)&
        Q(
            Q(category_id=question.category.id)|
            Q(targetType=Badge.targetTypes.General)
        
        ))
    for tag in question.tags.all():
        badges= badges.union(Badge.objects.filter(reason=Badge.reasons.SelfComments,tag=tag))
    badges=badges.difference(post.author.profile.badges.all())
    for badge in badges:
        if badge.count <= post.comments.count():
            post.author.profile.badges.add(badge)

def countVotesBadges(post):
    secondReason=Badge.reasons.QuestionVotes if post.type==Post.types.Question else Badge.reasons.AnswerVotes
    question=post.getQuestion()
    badges=Badge.objects.filter(
        Q(Q(reason=Badge.reasons.PostVotes)|Q(reason=secondReason))&
        Q(
            Q(category_id=question.category.id)|
            Q(targetType=Badge.targetTypes.General)
        
        ))
    for tag in question.tags.all():
        badges= badges.union(Badge.objects.filter(Q(Q(reason=Badge.reasons.PostVotes)|Q(reason=secondReason))& Q (tag=tag)))
    badges=badges.difference(post.author.profile.badges.all())
    for badge in badges:
        if badge.count <= post.votes:
            post.author.profile.badges.add(badge)


def countViewBadge(question):
    badges=Badge.objects.filter(
        Q(reason=Badge.reasons.Views)&
        Q(
            Q(category_id=question.category.id)|
            Q(targetType=Badge.targetTypes.General)
        
        ))
    for tag in question.tags.all():
        badges= badges.union(Badge.objects.filter(reason=Badge.reasons.Views,tag=tag))
    badges=badges.difference(question.post.author.profile.badges.all())
    for badge in badges:
        if badge.count <= question.views:
            question.post.author.profile.badges.add(badge)
