from django.template import Library

register=Library()

@register.inclusion_tag('content/templatetags/tag.html',name='tagLink')
def tagLink(tag):
    return {'tag':tag}
@register.inclusion_tag('content/templatetags/authorData.html',name='authodPostData')
def authodPostData(author):
    return{'author':author}