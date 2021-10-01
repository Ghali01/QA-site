from django.template import Library

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