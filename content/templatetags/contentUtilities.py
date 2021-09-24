from typing_extensions import ParamSpec
from django.db.models.expressions import F
from django.template import Library
from content.models import Voter
register=Library()

@register.inclusion_tag('content/templatetags/tag.html',name='tagLink')
def tagLink(tag):
    return {'tag':tag}
@register.inclusion_tag('content/templatetags/authorData.html',name='authodPostData')
def authodPostData(author):
    return{'author':author}

@register.filter('getVote')
def getVote(post,user):
    try:
        type=Voter.objects.get(post=post,user=user).type
        if type==True:
            return 'up'
        else:
            return 'down'
    except Voter.DoesNotExist:
        return False
@register.inclusion_tag('content/templatetags/commentItem.html')
def commentItem(comment,isSuperAdmin):
    return{
        'comment':comment,
        'isSuperAdmin':isSuperAdmin
        }