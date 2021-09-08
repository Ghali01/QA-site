from django.shortcuts import render,redirect
from django.urls import reverse
from interviewsquestions.utilities.authDecoratros import forActiveUser,userHasTags
from content.models import Category
from django.shortcuts import get_object_or_404
@forActiveUser
@userHasTags
def index(request,categoryID=-1):
    if request.user.is_authenticated and not request.user.is_anonymous:
        category=get_object_or_404(Category,id=categoryID) if not categoryID == -1 else None
        contxt={
            'category':category
        }
        return render(request,'content/index.html',contxt)
    else:
        return redirect(reverse('login-page'))