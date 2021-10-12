from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from ..models import EmailTemplate
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from misc.models import NewsUser
from django.utils.translation import gettext
from django.contrib.auth.models import User
def TenmplatesPage(request,language):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        templates=EmailTemplate.objects.filter(language=language)
        contxt={
            'templates':templates,
            'lang':language,
            'select': 'to' in request.GET,
            'toEmail':request.GET['to'] if 'to' in request.GET else None
        }
        return render(request,'dashboard/emailTemlates.html',context=contxt)
    else:
        return redirect("/dashboard/login")
def addTemplatePage(request,language):
    
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        contxt={
            'lang':language,
            'isNew':True
        }
        return render(request,'dashboard/addEditEmailTemplate.html',context=contxt)
    else:
        return redirect("/dashboard/login")

def addTemplate(request):

    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'temp-name' in request.POST and 'temp-body' in request.POST and 'language' in request.POST: 
            if request.POST['temp-name']:
                EmailTemplate.objects.create(
                    name=request.POST['temp-name'],
                    html=request.POST['temp-body'],
                    language=request.POST['language'],
                )
                messages.success(request,gettext('Template Created'))
                return redirect('/dashboard/templates/'+request.POST['language'])
            messages.error(request,gettext("Name can not be empty"))
            return redirect('/dashboard/add-template/'+request.POST['language'])


        else:
            messages.error(request,gettext("Value Error"))
            return redirect('/dashboard/templates/EN')
    else:
        return redirect("/dashboard/login")
def deleteTemplate(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'temp-id' in request.POST:
            try:
                ref=EmailTemplate.objects.get(pk=int(request.POST['temp-id']))
                ref.delete()
                return redirect('/dashboard/templates/'+ref.language)

            except EmailTemplate.DoesNotExist:
                messages.error(request,gettext("Template does not exists"))
                return redirect('/dashboard/templates/EN')
                
            except ValueError:
                messages.error(request,gettext("Invaild ID"))
                return redirect('/dashboard/templates/EN')
        else:
            messages.error(request,gettext("Value Error"))
            return redirect('/dashboard/templates/EN')
    else:
        return redirect("/dashboard/login")

def editTemplatePage(request,templateID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        try:
            template=EmailTemplate.objects.get(pk=templateID)
            contxt={
                'template':template,
                'lang':template.language,
                'isNew':False
            }
            return render(request,'dashboard/addEditEmailTemplate.html',contxt)
        except EmailTemplate.DoesNotExist:
            messages.error(request,gettext("template does not exists"))
            return redirect('/dashboard/templates/EN')
    else:
        return redirect("/dashboard/login")


def updateTemplate(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'temp-name' in request.POST and 'temp-body' in request.POST and 'temp-id' in request.POST: 

            try:
                template=EmailTemplate.objects.get(pk=int(request.POST['temp-id']))
                template.name=request.POST['temp-name']
                template.html=request.POST['temp-body']

                template.save()
                return redirect('/dashboard/edit-template/'+str(template.id))

            except EmailTemplate.DoesNotExist:
                messages.error(request,gettext("Reference does not exists"))
                return redirect('/dashboard/templates/EN')
                
            except ValueError:
                messages.error(request,gettext("Invaild ID"))
                return redirect('/dashboard/templates/EN')
        else:
            messages.error(request,gettext("Value Error"))
            return redirect('/dashboard/templates/EN')
    else:
        return redirect("/dashboard/login")


def sendEmailPage(request,language,templateID):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        try:
            if not templateID==-1:
                template=EmailTemplate.objects.get(pk=templateID)
            contxt={
                'template':template if not templateID==-1 else None,
                'lang':language,
                'select': 'to' in request.GET,
                'toEmail':request.GET['to'] if 'to' in request.GET else None

            }
            return render(request,'dashboard/sendEmail.html',context=contxt)
        except EmailTemplate.DoesNotExist:
            return redirect('/dashboard/templates/EN')

    else:
        return redirect("/dashboard/login")
def sendEmail(request):
    if request.user.is_authenticated and not request.user.is_anonymous and request.user.is_superuser:
        if 'msg-subject' in request.POST and 'msg-body' in request.POST and 'test-email' in request.POST and ('language' in request.POST or 'to-email' in request.POST ):
            if request.POST['msg-subject']:
                
                to=[]
                if request.POST['test-email']:
                    to=[request.POST['test-email'],]
                elif 'language' in request.POST:
                    users=User.objects.filter(profile__language=request.POST['language'].lower())
                    for user in users:
                        to.append(user.email)
                else:
                    to=[request.POST['to-email'],]
                subject = request.POST['msg-subject']
                html_message = request.POST['msg-body']
                plain_message = strip_tags(html_message)
                

                send_mail(subject, plain_message, None, to, html_message=html_message)
                messages.success(request,gettext('Email was sent'))
            else:
                messages.error(request,gettext("Subject Can not be empty"))

        else:
            messages.error(request,gettext("Value Error"))
        return redirect('/dashboard/templates/EN')


    else:
        return redirect("/dashboard/login")