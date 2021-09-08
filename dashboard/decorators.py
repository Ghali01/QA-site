from django.shortcuts import redirect
from django.urls import reverse


def forSuperAdmin(view):
    def decorators(request,*args,**kwargs):
            if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
                return view(request,*args,**kwargs)
            else:
                return redirect(reverse('dashboard:login'))
    return decorators