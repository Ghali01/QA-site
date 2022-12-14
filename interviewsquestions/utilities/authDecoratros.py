from django.urls import reverse
from django.shortcuts import redirect
def forActiveUser(viwe):
    def decorator(request,*arg,**kwargs):
        if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_active:
            return viwe(request,*arg,**kwargs)
        elif request.user.is_authenticated and not request.user.is_anonymous and not request.user.is_active:
            return  redirect(reverse('authusers:email-sent'))
        elif not request.user.is_authenticated or request.user.is_anonymous:
            return  redirect(reverse('authusers:login-page'))

    return decorator

def userHasTags(view):
    def decorator(request,*args,**kwargs):
        if request.user.profile.tags.count()>0:
            return view(request,*args,**kwargs)
        else:
            return redirect(reverse('authusers:select-tags'))
    return decorator


def forModerator(view):
    def decorator(request,*args,**kwargs):
        if request.user.profile.isModerator():
            return view(request,*args,**kwargs)
        else:
            return redirect(reverse('content:index'))
    return decorator

def forProfileOwner(view):
    def decorator(request,userID,*args,**kwarge):
        if userID==request.user.id:
            return view(request,userID,*args,**kwarge)
        else:
            return redirect(reverse('profiles:user-settings',kwargs={'userID':request.user.id}))

    return decorator