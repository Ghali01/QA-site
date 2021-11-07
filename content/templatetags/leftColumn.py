from django import template
from content.models import Category
from polls.models import Poll
from django.db.models import Q
from django.utils.translation import  get_language
import re 
register=template.Library()
@register.inclusion_tag('utilities/_categories.html',name='categories',takes_context=True)
@register.inclusion_tag('utilities/_categories_mob.html',name='categories_mob',takes_context=True)
def categories(context):
    categories=None    
    language=get_language()[:2]
    active=re.match('/categories|^/\d+',context['request'].path)
    
    try:
        categories=context['category'].toArray() if 'category' in context  and context['category'] else Category.objects.filter(language=language,parent=None)
        return {
            'categories':categories,
            'categoryName':context['category'].name if 'category' in context  and context['category'] else '',
            'active':active
        }
    except:
        pass

@register.inclusion_tag('utilities/_polls.html')
def polls(request):
    polls=Poll.objects.filter(Q(isOpened=True)&Q(~Q(resaults__user=request.user))&Q(language=get_language()[:2])&Q(Q(categories__isnull=True)|Q(categories=request.user.profile.category)))
    for tag in request.user.profile.tags.all():
        polls=polls.union(Poll.objects.filter(Q(isOpened=True)&Q(~Q(resaults__user=request.user))&Q(language=get_language()[:2])&Q(tags=tag)))
    return{
        'polls':polls,
        'active':'polls' in request.path
    }
@register.inclusion_tag('utilities/_polls_mob.html')
def pollsMob(user):
    polls=Poll.objects.filter(Q(isOpened=True)&Q(~Q(resaults__user=user))&Q(language=get_language()[:2])&Q(Q(categories__isnull=True)|Q(categories=user.profile.category)))
    for tag in user.profile.tags.all():
        polls=polls.union(Poll.objects.filter(Q(isOpened=True)&Q(~Q(resaults__user=user))&Q(language=get_language()[:2])&Q(tags=tag)))
    return{'polls':polls}