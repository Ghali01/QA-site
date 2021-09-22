from django.shortcuts import render,redirect
from django.urls import reverse
from content.models import Category
from django.contrib import messages
def categoriesPage(request,language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        categories=Category.objects.filter(language=language,parent=None)
        contxt={
            'lang':language,
            'categories':categories
        }
        return render(request, 'dashboard/categories.html',contxt)
    else:
        return redirect(reverse('dashboard:login'))
def addCategory(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'cate-id' in request.POST  and 'cate-name' in request.POST and 'cate-desc' in request.POST  and 'language' in request.POST:
            try:
                if request.POST['cate-name']:
                    category=Category()
                    category.name=request.POST['cate-name']
                    category.description=request.POST['cate-desc']
                    category.language=request.POST['language']
                    parent=int(request.POST['cate-id'])
                    if not parent ==-1:
                        category.parent=Category.objects.get(pk=parent)
                    category.save()
                else:
                    messages.error(request,'Name can not be empty')
            except (Category.DoesNotExist,ValueError):
                messages.error(request,'invalid id')
        return redirect(reverse('dashboard:categories',kwargs={'language':request.POST['language']}))
    else:
        return redirect(reverse('dashboard:login'))


def deleteCategory(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'cate-id' in request.POST  and 'language' in request.POST:
            try:
                Category.objects.get(pk=int(request.POST['cate-id'])).delete()
            except (Category.DoesNotExist,ValueError):
                messages.error(request,'invalid id')
            return redirect(reverse('dashboard:categories',kwargs={'language':request.POST['language']}))

        else:
            messages.error(request,'Values Error')

            return redirect(reverse('dashboard:categories',kwargs={'language':'en'}))

    else:
        return redirect(reverse('dashboard:login'))



def editCategory(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'cate-id' in request.POST and 'cate-name' in request.POST and 'cate-desc' in request.POST  and 'language' in request.POST:
            try:
                category=Category.objects.get(pk=int(request.POST['cate-id']))
                category.name=request.POST['cate-name']
                category.description=request.POST['cate-desc']
                category.save()
            except (Category.DoesNotExist,ValueError):
                messages.error(request,'invalid id')
            return redirect(reverse('dashboard:categories',kwargs={'language':request.POST['language']}))

        else:
            messages.error(request,'Values Error')

            return redirect(reverse('dashboard:categories',kwargs={'language':'en'}))

    else:
        return redirect(reverse('dashboard:login'))

