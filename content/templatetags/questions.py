from django.template import Library

register=Library()

@register.inclusion_tag('content/templatetags/questionItem.html')
def questionItem(question):
    return {'question':question}