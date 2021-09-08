from django import template
from content.models import Category

register=template.Library()
@register.inclusion_tag('utilities/_categories.html',name='categories',takes_context=True)
@register.inclusion_tag('utilities/_categories_mob.html',name='categories_mob',takes_context=True)
def categories(context):
    categories=None
    try:
        categories=context['category'].toArray() if 'category' in context  and context['category'] else Category.objects.filter(parent=None)
        return {
            'categories':categories,
        }
    except:
        pass