from django.shortcuts import redirect,render
from django.urls.base import reverse
from dashboard.decorators import forSuperAdmin
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

@forSuperAdmin
def usersPage(request):
    return render(request,'dashboard/users.html')  


@forSuperAdmin
def searchUsers(request):
    if 'search-text' in request.GET:
        users=[]
        if str(request.GET['search-text']).isdigit():
            user=User.objects.get(pk=int(request.GET['search-text']))
            users.append(user)
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
                    'perm':user.profile.get_permission_display()
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