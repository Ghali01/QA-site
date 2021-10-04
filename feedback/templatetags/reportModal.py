from django.template import Library
from feedback.models import FlagReason
register=Library()

@register.inclusion_tag('feedback/templatetags/reportModal.html')
def reportModal(type):
    reasons=FlagReason.objects.filter(type=type)
    return{'type':type,'reasons':reasons}