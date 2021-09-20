from django.template import Library
import html2text

register=Library()

@register.filter(name='html2text')
def htmlToText(html):
    tool=html2text.HTML2Text()
    tool.ignore_links=True
    tool.images_to_alt=True
    tool.ignore_tables=True
    return tool.handle(html)