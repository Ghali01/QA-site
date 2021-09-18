from django.template import Library

register=Library()

@register.inclusion_tag('content/templatetags/questionItem.html')
def questionItem(question):
    return {'question':question}

    
@register.inclusion_tag('content/templatetags/question.html')
def question(question,request):
    return {'question':question,'request':request}

@register.inclusion_tag('content/templatetags/answer.html')
def answer(answer,request):
    return {'ans':answer,'request':request}

    