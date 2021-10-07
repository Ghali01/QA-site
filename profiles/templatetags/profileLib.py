import mimetypes
from django.template import Library
from django.urls.base import reverse
import base64
from interviewsquestions.settings import MEDIA_ROOT
from mimetypes import guess_type
import os
register=Library()

@register.inclusion_tag('profiles/templatetags/badgeItem.html')
def badgeItem(badge):
    return {'badge':badge}

@register.inclusion_tag('profiles/templatetags/followerItem.html')
def followerItem(person,user):
    return{
        'person':person,
        'user':user
    }

@register.simple_tag
def smImgProfile(user):
    fileNameO=user.profile.image.name 
    arrN=fileNameO.split('/')
    arrN[-1]='sm-'+arrN[-1]
    fileName='/'.join(arrN) 
    if not os.path.exists(str(MEDIA_ROOT)+'/'+fileName):
        fileName=fileNameO
    file =open(str(MEDIA_ROOT)+'/'+fileName,'rb')
    type=guess_type(fileName)[0]
    b64=base64.b64encode(file.read()).decode('utf-8')
    date=f'data:{type};base64, {b64}'
    return date