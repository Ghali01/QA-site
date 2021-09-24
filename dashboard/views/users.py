from content.models import Post
from django.shortcuts import get_object_or_404, redirect,render
from django.urls.base import reverse
from dashboard.decorators import forSuperAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
from authusers.models import BanedUser
import json

@forSuperAdmin
def usersPage(request):
    return render(request,'dashboard/users.html')  


@forSuperAdmin
def searchUsers(request):
    if 'search-text' in request.GET:
        users=[]
        if str(request.GET['search-text']).isdigit():
            try:
                user=User.objects.get(pk=int(request.GET['search-text']))
                users.append(user)
            except User.DoesNotExist:
                pass
        else:
            users=User.objects.filter(username__contains=request.GET['search-text'])
        data=[]
        for user in users:
            try:
                data.append({
                    'userName':user.username,
                    'fullName':user.first_name,
                    'id':user.id,
                    'email':user.email,
                    'perm':user.profile.get_permission_display(),
                    'isBaned':str(user.profile.isBaned())
                })
            except:
                pass
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse('Value Erorr')
@forSuperAdmin
def setUserPermission(request):
    if 'perm' in request.POST and 'user-id' in request.POST:
        try:
            user=User.objects.get(pk=int(request.POST['user-id']))

            if request.POST['perm']=='SA':
                user.is_superuser=True
                user.save()
           
            user.profile.permission=request.POST['perm']
            user.profile.save()
            
        except (User.DoesNotExist,ValueError):
            pass

    return redirect(reverse('dashboard:users'))



@forSuperAdmin
def pruneUser(request):
    if 'user-id' in request.POST:

        if 'questions' in request.POST:
            questions=Post.objects.filter(author_id=request.POST['user-id'],type=Post.types.Question)
            questions.update(isPublished=False)
        if 'answers' in request.POST:
            answers=Post.objects.filter(author_id=request.POST['user-id'],type=Post.types.Answer)
            answers.update(isPublished=False)
        
    return redirect(reverse('dashboard:users'))


@forSuperAdmin
def toggleBanUser(request):
    if 'user-id' in request.POST:
        try:
            user=get_object_or_404(User,id=int(request.POST['user-id']))
            if not BanedUser.objects.filter(user=user).exists():
                BanedUser.objects.create(user=user)        
            else:
                BanedUser.objects.get(user=user).delete()
        except ValueError:
            pass
    return redirect(reverse('dashboard:users'))
